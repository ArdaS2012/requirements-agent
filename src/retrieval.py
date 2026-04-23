import psycopg
from pgvector.psycopg import register_vector

from .config import DB_URL, cross_encoder
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

def rerank_query(query, results):
    if not results:
        return []

    contents = [row[0] for row in results]
    query = [query] #transform to list for cross encoder
    pairs = [[query[0], content] for content in contents]
    scores = cross_encoder.predict(pairs)

    reranked_results = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)
    return [result for result, score in reranked_results]