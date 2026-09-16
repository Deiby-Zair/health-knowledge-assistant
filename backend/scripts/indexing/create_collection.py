from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from src.config import get_settings
from src.services.embeddings.embedding_manager import get_embedding_provider


def main():
    embedder = get_embedding_provider()

    client = QdrantClient(
        url= get_settings().qdrant_url,
        api_key=get_settings().qdrant_api_key,
    )
    
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