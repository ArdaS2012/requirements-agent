import os

import psycopg
from pgvector.psycopg import register_vector
from psycopg.types.json import Jsonb

from .config import DB_URL, base_path, path_to_raw
from .embeddings import fake_embedding
from .pdf_processing import process_pdfs


def process_ingestion():
    for i,doc_path in enumerate(path_to_raw):
        document_id = f"doc-{i}"
        source_path = os.path.join(base_path, doc_path)
        content = process_pdfs(source_path)
        #chunks = chunk_document(content, source_path)
        chunks = []
        with psycopg.connect(DB_URL) as conn:
            register_vector(conn)

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
                            fake_embedding(chunk["content"]),
                        ),
                    )

            conn.commit()

        print(f"Inserted {len(chunks)} chunks for {doc_path} into rag_chunks.")
