import psycopg
from pgvector.psycopg import register_vector

from .config import DB_URL
from .embeddings import create_embedding

def process_query(query):
    query = [query] #transform to list for embedding function
    query_embedding = create_embedding(query)[0] #get the embedding vector from the list
    with psycopg.connect(DB_URL) as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT content, metadata, embedding <=> %s::vector AS distance
                FROM rag_chunks
                ORDER BY distance
                LIMIT 5;
                """,
                (query_embedding,),
            )
            results = cur.fetchall()


    return results