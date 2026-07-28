from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from backend.src.embeddings.embedding_manager import get_embedding_provider

BASE_DIR = Path(__file__).resolve().parents[2]
QDRANT_PATH = BASE_DIR / "backend" / "qdrant_data"

def main():
    embedder = get_embedding_provider()

    client = QdrantClient(path=str(QDRANT_PATH))

    client.delete_collection("minsalud_rag")

    client.create_collection(
        collection_name="minsalud_rag",
        vectors_config=VectorParams(
            size=embedder.dimension,
            distance=Distance.COSINE
        )
    )

    print("Collection created")
    
if __name__ == "__main__":
    main()