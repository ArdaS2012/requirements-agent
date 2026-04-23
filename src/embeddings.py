import os
from .config import embedding_model

# TODO: Remove fake_embedding once the real pipeline is fully validated
def fake_embedding(text: str, dim: int = 1536) -> list[float]:
    """Deterministic stub embedding for local testing without a real model.

    Produces a sparse vector whose first three dimensions encode crude
    text-length and keyword statistics.  Do NOT use in production.
    """
    vec = [0.0] * dim
    vec[0] = min(len(text) / 1000.0, 1.0)   # normalised character count
    vec[1] = text.lower().count("rag")       # keyword frequency feature
    vec[2] = text.lower().count("postgres")  # keyword frequency feature
    return vec


def create_embedding(text: list[str]) -> list[list[float]]:
    """Encode a list of strings into dense vectors using the shared bi-encoder.

    The model (all-MiniLM-L6-v2) is loaded once in config.py and reused here
    to avoid reloading weights on every call.

    Args:
        text: Strings to encode.  Can be chunks (at ingestion time) or a
              single-element list containing the user's query.

    Returns:
        A list of float vectors, one per input string.
    """
    embeddings = []
    for t in text:
        # encode() returns a NumPy array; .tolist() converts it to plain Python
        embedding = embedding_model.encode(t).tolist()
        embeddings.append(embedding)
    return embeddings
