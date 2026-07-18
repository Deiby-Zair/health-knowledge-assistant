from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Conexión a Qdrant local
client = QdrantClient(path="./qdrant_data")

# Modelo de embeddings
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Consulta del usuario
query = "¿Qué es la afiliación al sistema de salud?"

# Embedding de la consulta
query_vector = model.encode(query).tolist()

# Búsqueda semántica
results = client.query_points(
    collection_name="minsalud_rag",
    query=query_vector,
    limit=3
).points

# Mostrar resultados
for r in results:
    print("Score:", round(r.score, 3))
    print("Fuente:", r.payload.get("source"))
    print("Texto:", r.payload.get("text")[:120])
    print("-" * 50)