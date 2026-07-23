from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
QDRANT_PATH = BASE_DIR / "qdrant_data"

client = QdrantClient(path=str(QDRANT_PATH))

client.create_collection(
    collection_name="minsalud_rag",
    vectors_config=VectorParams(
        size=384,  # dimensión de all-MiniLM-L6-v2
        distance=Distance.COSINE
    )
)

print("Collection created")