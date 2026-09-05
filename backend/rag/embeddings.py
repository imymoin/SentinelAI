from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Local sentence-transformer embedding model.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.model = SentenceTransformer(model_name)

    def embed_documents(
        self,
        documents: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple documents.
        """

        if not documents:
            return []

        embeddings = self.model.encode(
            documents,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate an embedding for a query.
        """

        if not query:
            return []

        embedding = self.model.encode(
            query,
            normalize_embeddings=True,
        )

        return embedding.tolist()