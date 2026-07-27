import os

from .sentence_transformer_provider import SentenceTransformerProvider
from .gemini_provider import GeminiEmbeddingProvider

PROVIDER = os.getenv("EMBEDDING_PROVIDER", "sentence_transformers")
MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)


def get_embedding_provider():

    if PROVIDER == "sentence_transformers":
        return SentenceTransformerProvider(MODEL)

    if PROVIDER == "gemini":
        return GeminiEmbeddingProvider(MODEL)

    raise ValueError(f"Embedding provider '{PROVIDER}' not supported.")