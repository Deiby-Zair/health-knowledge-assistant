from src.config import get_settings

from .gemini_provider import GeminiEmbeddingProvider
from .sentence_transformer_provider import SentenceTransformerProvider

def get_embedding_provider():

    settings = get_settings()

    provider = settings.embedding_provider
    model = settings.embedding_model

    print(f"Using embedding provider: {provider} with model: {model}")

    if provider == "sentence_transformers":
        return SentenceTransformerProvider(model)

    if provider == "gemini":
        from google import genai
        client = genai.Client(api_key=settings.gemini_api_key)

        return GeminiEmbeddingProvider(client, model, 768)

    raise ValueError(f"Embedding provider '{provider}' not supported.")