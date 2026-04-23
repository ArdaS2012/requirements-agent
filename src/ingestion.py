import os

import psycopg
from pgvector.psycopg import register_vector
from psycopg.types.json import Jsonb

from .config import DB_URL, base_path, path_to_raw
from .pdf_processing import process_page


def process_ingestion():
    """Ingest all PDFs in data/raw/ into the rag_chunks table.

    For each PDF the function:
    1. Iterates over pages via process_page() (a generator).
    2. Assembles chunk records (text + embedding + metadata).
    3. Inserts them into PostgreSQL and commits after every page.

    chunk_index is a document-scoped counter so chunks can be retrieved
    in their original reading order when needed.
    """
    for i, doc_path in enumerate(path_to_raw):
        # Assign a stable string ID to each document (e.g. "doc-0", "doc-1")
        document_id = f"doc-{i}"
        source_path = os.path.join(base_path, doc_path)

        with psycopg.connect(DB_URL) as conn:
            # register_vector makes psycopg aware of the pgvector type so that
            # Python lists are automatically cast to/from PostgreSQL vectors
            register_vector(conn)
            total_chunks = 0

            # process_page is a generator — each yield covers one PDF page
            for page_content in process_page(source_path):
                # Build chunk dicts by zipping the parallel lists returned per page
                chunks = [
                    {
                        "chunk_index": total_chunks + chunk_id,  # global index within this doc
                        "content": text,
                        "metadata": page_content["metadata"],
                        "embedding": embedding,
                    }
                    for chunk_id, text, embedding in zip(
                        page_content["chunk_id"],
                        page_content["chunk_content"],
                        page_content["embeddings"],
                    )
                ]

                with conn.cursor() as cur:
                    for chunk in chunks:
                        cur.execute(
                            """
                            INSERT INTO rag_chunks
                                (document_id, chunk_index, content, metadata, embedding)
                            VALUES
                                (%s, %s, %s, %s, %s)
                            """,
                            (
                                document_id,
                                chunk["chunk_index"],
                                chunk["content"],
                                Jsonb(chunk["metadata"]),   # store metadata as JSONB
                                chunk["embedding"],
                            ),
                        )

                # Commit after each page so that partial progress is preserved
                # if the process is interrupted mid-document
                conn.commit()
                total_chunks += len(chunks)

        print(f"Inserted {total_chunks} chunks for {doc_path} into rag_chunks.")


def reset_table():
    """Truncate the rag_chunks table and reset its auto-increment counter.

    Call this before re-ingesting documents to avoid duplicate entries.
    TRUNCATE ... RESTART IDENTITY is equivalent to DELETE + sequence reset
    but is significantly faster on large tables.
    """
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE rag_chunks RESTART IDENTITY;")
        conn.commit()
    print("rag_chunks table truncated.")
