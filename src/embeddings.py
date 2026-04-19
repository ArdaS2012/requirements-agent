import os
from .config import embedding_model
#Todo: Add real embedding and API call
def fake_embedding(text: str, dim: int = 1536) -> list[float]:
    # Demo only: creates a deterministic vector so you can insert rows now.
    # In a real app, replace this with your embedding model/API call.
    vec = [0.0] * dim
    vec[0] = min(len(text) / 1000.0, 1.0)
    vec[1] = text.lower().count("rag")
    vec[2] = text.lower().count("postgres")
    return vec

def create_embedding(text: list[str]) -> list[float]:
    embeddings = []
    for t in text:
        embedding = embedding_model.encode(t).tolist()
        embeddings.append(embedding)
    return embeddings
