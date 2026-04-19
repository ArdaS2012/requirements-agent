import os

from dotenv import load_dotenv
from openai import OpenAI

DB_URL = "postgresql://postgres:password@localhost:5432/requirements"
base_path = "/home/arda/Desktop/Projects/requirement_project/database_raw"
path_to_raw = os.listdir(base_path)

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)
