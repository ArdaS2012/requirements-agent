import os

from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
DB_URL = "postgresql://postgres:password@localhost:5432/requirements"
base_path = "/home/arda/Desktop/Projects/requirement_project/data/raw"
path_to_raw = os.listdir(base_path)

load_dotenv()
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)
