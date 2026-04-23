import os
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import CrossEncoder, SentenceTransformer
from groq import Groq
from .security import SecureLLMPipeline

# PostgreSQL connection string — loaded from DATABASE_URL env var, with a
# localhost default for local development. Never commit real credentials.
DB_URL = os.environ.get("DATABASE_URL", "")

# Root directory that contains the source PDF files to be ingested.
# Uses a path relative to this file so the project works on any machine.
base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")

# List of PDF filenames discovered at startup; used by the ingestion pipeline
path_to_raw = os.listdir(base_path)

# Load GROQ_API_KEY and HF_TOKEN from the .env file
load_dotenv()

# Bi-encoder used to convert text chunks and queries into dense vectors.
# all-MiniLM-L6-v2 produces 384-dimensional embeddings and is fast on CPU.
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# OpenAI-compatible client pointed at HuggingFace's inference router.
# Used for optional VLM image description calls in pdf_processing.py.
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

# Groq client used for the main chat-completion calls (fast LLM inference)
client_agent = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Wraps client_agent with prompt-injection filtering and output validation
llm_pipeline = SecureLLMPipeline(client_agent)

# Cross-encoder used to rerank the top-k candidates from vector search.
# ms-marco-MiniLM-L-6-v2 scores (query, passage) pairs jointly for precision.
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# Maximum number of conversation turns to keep in the context window
NR_HISTORY = 10

# System prompt that governs the LLM's behaviour throughout a conversation.
# It instructs the model to stay strictly within the retrieved document content.
AGENT_SYSTEM_PROMPT = "You are an assistant for software requirements analysis. You will be provided questions to requirements of a specific document and need to answer as precisely as possible based on the content of the document." \
" If you don't know the answer, say you don't know. Always be concise and precise in your answers. Do not provide any information that is not explicitly stated in the document. Always refer to the document content when answering questions." \
"You will retrieve relevant information from the document based on the question and use that information to answer the question. You will not make any assumptions or guesses about the content of the document. Always provide answers that are directly supported by the content of the document."