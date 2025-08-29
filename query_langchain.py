import os
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

# --- config ---
COLLECTION_NAME = "markdown_docs"
EMBED_MODEL = "text-embedding-3-small"

# --- API key ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Qdrant ---
qdrant = QdrantClient(location="localhost", port=6333)

# --- user query ---
query = input("❓ Enter your question: ")

# create embedding
query_embedding = client.embeddings.create(input=query, model=EMBED_MODEL).data[0].embedding

# search
results = qdrant.search(
    collection_name=COLLECTION_NAME,
    query_vector=query_embedding,
    limit=5
)

print("\n📌 Found relevant chunks:\n")
for i, r in enumerate(results, start=1):
    print(f"--- Chunk {i} (score={r.score:.3f}) ---")
    print(r.payload.get("text", ""))
    print()
