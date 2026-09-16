import json
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

from src.config import get_settings
from src.services.embeddings.embedding_manager import get_embedding_provider


BASE_DIR = Path(__file__).resolve().parents[2]
CHUNKS_DIR = BASE_DIR / "data" / "chunks"

INPUT_FILES = [
    "faq_chunks.json",
    "glossary_chunks.json",
    "pdf_chunks.json",
]

COLLECTION_NAME = "minsalud_rag"
UPSERT_BATCH_SIZE = 50


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    settings = get_settings()

    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        timeout=60,
    )

    # Embedding provider
    embedder = get_embedding_provider()

    # Load chunks
    chunks = []

    for filename in INPUT_FILES:
        chunks.extend(load_json(CHUNKS_DIR / filename))

    print(f"Loaded {len(chunks)} chunks")

    # Generate embeddings
    texts = [chunk["text"] for chunk in chunks]

    print("Generating embeddings...")
    embeddings = embedder.embed(texts)

    if len(embeddings) != len(chunks):
        raise ValueError(
            f"Number of embeddings ({len(embeddings)}) "
            f"does not match number of chunks ({len(chunks)})"
        )

    dimension = len(embeddings[0])

    print(f"Embedding dimension: {dimension}")

    # Create collection if it does not exist
    collections = client.get_collections()
    collection_names = [collection.name for collection in collections.collections]

    if COLLECTION_NAME not in collection_names:
        print(f"Creating collection '{COLLECTION_NAME}'...")

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=dimension,
                distance=Distance.COSINE,
            ),
        )

    # Build points
    points = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id=i,
                vector=embedding,
                payload={
                    "text": chunk["text"],
                    **chunk["metadata"],
                },
            )
        )

    # Upload to Qdrant in batches
    total_batches = (
        len(points) + UPSERT_BATCH_SIZE - 1
    ) // UPSERT_BATCH_SIZE

    for batch_number, start in enumerate(
        range(0, len(points), UPSERT_BATCH_SIZE),
        start=1,
    ):
        batch = points[start:start + UPSERT_BATCH_SIZE]

        print(
            f"Qdrant upsert "
            f"{batch_number}/{total_batches} "
            f"({len(batch)} points)"
        )

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch,
            wait=True,
        )

    print(
        f"{len(points)} chunks ingested into "
        f"Qdrant collection '{COLLECTION_NAME}'"
    )


if __name__ == "__main__":
    main()