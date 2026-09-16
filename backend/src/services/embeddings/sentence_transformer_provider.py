from sentence_transformers import SentenceTransformer

from .base import EmbeddingProvider


class SentenceTransformerProvider(EmbeddingProvider):

    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts).tolist()
    
    @property
    def dimension(self):
        return self.model.get_embedding_dimension()