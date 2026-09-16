import json

from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from src.config import get_settings
from src.services.embeddings.embedding_manager import get_embedding_provider

BASE_DIR = Path(__file__).resolve().parents[2]
CHUNKS_DIR = BASE_DIR / "data" / "chunks"

INPUT_FILES = [
    "faq_chunks.json",
    "glossary_chunks.json",
    "pdf_chunks.json",
]

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def main():
    #  local conection
    client = QdrantClient(
        url= get_settings().qdrant_url,
        api_key=get_settings().qdrant_api_key,
    )
    # Embeddings model
    embedder = get_embedding_provider()
    
    chunks = []
    for filename in INPUT_FILES:
        chunks.extend(load_json(CHUNKS_DIR / filename))

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