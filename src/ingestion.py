import os

import psycopg
from pgvector.psycopg import register_vector
from psycopg.types.json import Jsonb

from .config import DB_URL, base_path, path_to_raw
from .pdf_processing import process_page


def process_ingestion():
    for i,doc_path in enumerate(path_to_raw):
        document_id = f"doc-{i}"
        source_path = os.path.join(base_path, doc_path)
        with psycopg.connect(DB_URL) as conn:
            register_vector(conn)
            total_chunks = 0
            for page_content in process_page(source_path):
                chunks = [
                    {
                        "chunk_index": total_chunks + chunk_id,
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
                                Jsonb(chunk["metadata"]),
                                chunk["embedding"],
                            ),
                        )
                conn.commit()
                total_chunks += len(chunks)

        print(f"Inserted {total_chunks} chunks for {doc_path} into rag_chunks.")


def reset_table():
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE rag_chunks RESTART IDENTITY;")
        conn.commit()
    print("rag_chunks table truncated.")
