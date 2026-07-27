from .base import EmbeddingProvider

class GeminiEmbeddingProvider(EmbeddingProvider):

    def __init__(self, client, model):
        self.client = client
        self.model = model

    def embed(self, texts):
        vectors = []

        for text in texts:
            response = self.client.models.embed_content(
                model=self.model,
                contents=text,
            )

            vectors.append(response.embeddings[0].values)

        return vectors
    
    @property
    def dimension(self):
        return self.model.get_embedding_dimension()