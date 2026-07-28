from pathlib import Path

from qdrant_client import QdrantClient

from backend.src.embeddings.embedding_manager import get_embedding_provider
from backend.src.rag.schemas import Source

BASE_DIR = Path(__file__).resolve().parents[2]
QDRANT_PATH = BASE_DIR / "qdrant_data"

COLLECTION_NAME = "minsalud_rag"
MIN_SCORE = 0.5

qdrant = QdrantClient(path=str(QDRANT_PATH))
embedder = get_embedding_provider()


def retrieve_context(question: str, limit: int = 5):
    query_vector = embedder.embed([question])[0]

    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
    ).points

    if not results:
        return "", []

    # Filtrar por similitud
    results = [
        r
        for r in results
        if r.score is not None and r.score >= MIN_SCORE
    ]

    if not results:
        return "", []

    context = "\n\n".join(
        r.payload["text"].strip()
        for r in results
    )

    sources = []

    seen = set()

    for r in results:

        source = Source(
            title=r.payload.get("source", "Sin título"),
            location = next(
                (
                    f"{k}: {r.payload[k]}"
                    for k in ("page", "term", "question")
                    if r.payload.get(k) is not None
                ),
                None,
            ),
            score=round(r.score, 3),
        )

        key = (source.title, source.location)

        if key not in seen:
            seen.add(key)
            sources.append(source)

    return context, sources