from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(path="./qdrant_data")

client.create_collection(
    collection_name="minsalud_rag",
    vectors_config=VectorParams(
        size=384,  # dimensión de all-MiniLM-L6-v2
        distance=Distance.COSINE
    )
)

print("Collection created")