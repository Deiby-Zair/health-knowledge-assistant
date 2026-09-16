import time

from google.genai.errors import ClientError

from .base import EmbeddingProvider


class GeminiEmbeddingProvider(EmbeddingProvider):

    BATCH_SIZE = 50

    def __init__(self, client, model, dimension):
        self.client = client
        self.model = model
        self._dimension = dimension

    def embed(self, texts):
        vectors = []

        total_batches = (len(texts) + self.BATCH_SIZE - 1) // self.BATCH_SIZE

        for i in range(0, len(texts), self.BATCH_SIZE):
            batch = texts[i:i + self.BATCH_SIZE]
            batch_number = i // self.BATCH_SIZE + 1

            print(
                f"Generating embeddings: "
                f"batch {batch_number}/{total_batches} "
                f"({len(batch)} texts)"
            )

            for attempt in range(5):
                try:
                    response = self.client.models.embed_content(
                        model=self.model,
                        contents=batch,
                    )

                    vectors.extend(
                        embedding.values
                        for embedding in response.embeddings
                    )

                    break

                except ClientError as e:
                    if e.code != 429:
                        raise

                    wait_time = 2 ** attempt

                    print(
                        f"Rate limit reached. "
                        f"Retrying in {wait_time}s..."
                    )

                    time.sleep(wait_time)

            else:
                raise RuntimeError(
                    f"Failed to generate embeddings for batch "
                    f"{batch_number} after 5 attempts."
                )

        return vectors

    @property
    def dimension(self):
        return self._dimension