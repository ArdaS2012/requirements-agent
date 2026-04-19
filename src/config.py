import os

from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from groq import Groq
DB_URL = "postgresql://postgres:password@localhost:5432/requirements"
base_path = "/home/arda/Desktop/Projects/requirement_project/data/raw"
path_to_raw = os.listdir(base_path)

load_dotenv()
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)
client_agent = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
AGENT_SYSTEM_PROMPT = "You are an assistant for software requirements analysis. You will be provided questions to requirements of a specific document and need to answer as precisely as possible based on the content of the document." \
" If you don't know the answer, say you don't know. Always be concise and precise in your answers. Do not provide any information that is not explicitly stated in the document. Always refer to the document content when answering questions." \
"You will retrieve relevant information from the document based on the question and use that information to answer the question. You will not make any assumptions or guesses about the content of the document. Always provide answers that are directly supported by the content of the document."