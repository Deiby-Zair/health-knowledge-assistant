import json

from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer

#  local conection
client = QdrantClient(path="./qdrant_data")

# Modelo de embeddings
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FAQ = PROJECT_ROOT / "data" / "chunks" / "faq_chunks.json"
INPUT_GLOSSARY = PROJECT_ROOT / "data" / "chunks" / "glossary_chunks.json"
INPUT_PDF = PROJECT_ROOT / "data" / "chunks" / "pdf_chunks.json"

with open(INPUT_FAQ, "r", encoding="utf-8") as f:
    faq_chunks = json.load(f)

with open(INPUT_GLOSSARY, "r", encoding="utf-8") as f:
    glossary_chunks = json.load(f)

with open(INPUT_PDF, "r", encoding="utf-8") as f:
    pdf_chunks = json.load(f)

chunks = faq_chunks + glossary_chunks + pdf_chunks

points = []

for i, chunk in enumerate(chunks):
    embedding = model.encode(chunk["text"]).tolist()

    points.append(
        PointStruct(
            id=i,
            vector=embedding,
            payload={
                "text": chunk["text"],
                **chunk["metadata"]
            }
        )
    )

client.upsert(
    collection_name="minsalud_rag",
    points=points
)

print(f"{len(points)} chunks ingested into Qdrant collection 'minsalud_rag'")