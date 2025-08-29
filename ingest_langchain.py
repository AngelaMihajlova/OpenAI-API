import os
import glob
import uuid
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm

# --- config ---
DATA_GLOB = "data/data/*.md"
COLLECTION_NAME = "markdown_docs"
EMBED_MODEL = "text-embedding-3-small"
BATCH_SIZE = 64  # set to 1 to disable batching

# --- API key ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Qdrant (local Docker) ---
qdrant = QdrantClient("localhost", port=6333)

# Create/reset collection (1536 dims for text-embedding-3-small)
qdrant.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
)

# --- LangChain Text Splitter ---
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
)

# --- Collect files ---
files = glob.glob(DATA_GLOB)

if not files:
    print("No .md files found at", DATA_GLOB)
    raise SystemExit(0)

# --- Outer progress: files ---
for file_path in tqdm(files, desc="Files", position=0):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 1) Chunk
    chunks = text_splitter.split_text(text)
    if not chunks:
        tqdm.write(f"⚠️  No chunks for {os.path.basename(file_path)}")
        continue

    # 2) Embeddings + upsert, with inner progress
    #    We'll do batched upserts for speed and a smoother progress bar.
    inner_bar = tqdm(total=len(chunks), desc=f"Chunks: {os.path.basename(file_path)}", position=1, leave=False)

    # batch accumulators
    batch_points = []

    for idx, chunk in enumerate(chunks):
        # embeddings
        emb = client.embeddings.create(
            model=EMBED_MODEL,
            input=chunk
        ).data[0].embedding

        # deterministic UUID (stable across runs for same file+idx)
        point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{os.path.abspath(file_path)}#{idx}"))

        batch_points.append(
            models.PointStruct(
                id=point_id,
                vector=emb,
                payload={
                    "filename": os.path.basename(file_path),
                    "chunk_id": idx,
                    "text": chunk
                }
            )
        )

        # flush in batches
        if len(batch_points) >= BATCH_SIZE:
            qdrant.upsert(collection_name=COLLECTION_NAME, points=batch_points)
            batch_points.clear()

        inner_bar.update(1)

    # flush remaining
    if batch_points:
        qdrant.upsert(collection_name=COLLECTION_NAME, points=batch_points)

    inner_bar.close()

print("✅ Done: documents ingested into Qdrant with progress bars.")