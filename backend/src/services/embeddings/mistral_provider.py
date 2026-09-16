from mistralai.client import Mistral

from src.config import get_settings

from .base import EmbeddingProvider


class MistralEmbeddingProvider(EmbeddingProvider):

    def __init__(
        self,
        model_name: str = "mistral-embed",
        batch_size: int = 32,
    ):
        
        api_key = get_settings().mistral_api_key
        
        if not api_key:
            raise ValueError("MISTRAL_API_KEY not configured")

        self.client = Mistral(api_key=api_key)
        self.model_name = model_name
        self.batch_size = batch_size


        # mistral-embed generate vectors with 1024 dimensions
        self._dimension = 1024

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        embeddings = []
        total_batches = (
            len(texts) + self.batch_size - 1
        ) // self.batch_size

        for batch_number, i in enumerate(
            range(0, len(texts), self.batch_size),
            start=1,
        ):
            batch = texts[i:i + self.batch_size]

            print(
                f"Embedding batch {batch_number}/{total_batches} "
                f"({len(batch)} textos)"
            )

            response = self.client.embeddings.create(
                model=self.model_name,
                inputs=batch,
            )

            embeddings.extend(
                item.embedding
                for item in response.data
            )

        return embeddings

    @property
    def dimension(self):
        return self._dimension