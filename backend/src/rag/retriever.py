from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
QDRANT_PATH = BASE_DIR / "qdrant_data"

# Inicializar una sola vez
qdrant = QdrantClient(path=str(QDRANT_PATH))
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def retrieve_context(question: str, limit: int = 3):
    # 1. Embedding de la pregunta
    query_vector = embed_model.encode(question).tolist()

    # 2. Buscar en Qdrant
    results = qdrant.query_points(
        collection_name="minsalud_rag",
        query=query_vector,
        limit=limit
    ).points

    # 3. Construir contexto
    context = "\n\n".join(r.payload["text"] for r in results)

    # 4. Extraer fuentes únicas
    sources = list({r.payload.get("source") for r in results})

    return context, sources