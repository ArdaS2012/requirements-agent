import psycopg
from pgvector.psycopg import register_vector

from .config import DB_URL, cross_encoder
from .embeddings import create_embedding


def process_query(query: str) -> list:
    """Retrieve the top-5 chunks most similar to the query via cosine distance.

    The query string is embedded with the same bi-encoder used at ingestion
    time, then compared against all stored vectors using the pgvector
    ``<=>`` (cosine distance) operator.  Lower distance = more similar.

    Args:
        query: The raw user question.

    Returns:
        A list of (content, metadata, distance) tuples ordered by ascending
        cosine distance (most relevant first).
    """
    # Wrap in a list because create_embedding expects a batch
    query_embedding = create_embedding([query])[0]  # extract the single vector

    with psycopg.connect(DB_URL) as conn:
        register_vector(conn)  # make psycopg recognise the vector type
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


def rerank_query(query: str, results: list) -> list:
    """Rerank vector-search candidates using a cross-encoder model.

    A cross-encoder jointly encodes the (query, passage) pair and produces a
    relevance score that is more accurate than bi-encoder cosine distance,
    at the cost of higher latency.  This is applied only to the small set of
    candidates returned by process_query().

    Args:
        query:   The original user question.
        results: Candidate rows from process_query() — each row is
                 (content, metadata, distance).

    Returns:
        The same rows re-ordered by cross-encoder score (highest first).
    """
    if not results:
        return []

    contents = [row[0] for row in results]  # extract text from each result row

    # cross_encoder.predict() expects a list of [query, passage] pairs
    pairs = [[query, content] for content in contents]
    scores = cross_encoder.predict(pairs)

    # zip results with their scores, sort descending (higher score = more relevant)
    reranked_results = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)
    # Return (content, metadata, distance, cross_encoder_score) tuples
    return [(result[0], result[1], result[2], float(score)) for result, score in reranked_results]