import json
import os
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from backend.src.embeddings.embedding_manager import get_embedding_provider

BASE_DIR = Path(__file__).resolve().parents[1]
QDRANT_PATH = BASE_DIR / "qdrant_data"

INPUT_FAQ = BASE_DIR / "data" / "chunks" / "faq_chunks.json"
INPUT_GLOSSARY = BASE_DIR / "data" / "chunks" / "glossary_chunks.json"
INPUT_PDF = BASE_DIR / "data" / "chunks" / "pdf_chunks.json"

def main():
    #  local conection
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )
    # Embeddings model
    embedder = get_embedding_provider()

    with open(INPUT_FAQ, "r", encoding="utf-8") as f:
        faq_chunks = json.load(f)

    with open(INPUT_GLOSSARY, "r", encoding="utf-8") as f:
        glossary_chunks = json.load(f)

    with open(INPUT_PDF, "r", encoding="utf-8") as f:
        pdf_chunks = json.load(f)

    chunks = faq_chunks + glossary_chunks + pdf_chunks

    texts = [chunk["text"] for chunk in chunks]

    embeddings = embedder.embed(texts)

    points = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
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
    
if __name__ == "__main__":
    main()