from pathlib import Path

import chromadb

from backend.rag.embeddings import EmbeddingModel


class ChromaVectorStore:
    """
    Local ChromaDB vector store.
    """

    def __init__(
        self,
        persist_directory: str = "data/chroma",
        collection_name: str = "sentinel_documents",
    ):
        self.persist_directory = Path(
            persist_directory
        )

        self.persist_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name
            )
        )

        self.embedding_model = EmbeddingModel()

    def add_documents(
        self,
        documents: list[str],
        metadatas: list[dict] | None = None,
        ids: list[str] | None = None,
    ):
        """
        Add documents to ChromaDB.
        """

        if not documents:
            return

        embeddings = (
            self.embedding_model.embed_documents(
                documents
            )
        )

        if ids is None:
            ids = [
                f"doc_{self.collection.count() + i}"
                for i in range(len(documents))
            ]

        if metadatas is None:
            metadatas = [
                {
                    "source": "unknown"
                }
                for _ in documents
            ]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[dict]:
        """
        Search ChromaDB for the most relevant chunks.
        """

        if not query.strip():
            return []

        if self.collection.count() == 0:
            return []

        query_embedding = (
            self.embedding_model.embed_query(
                query
            )
        )

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        documents = results.get(
            "documents",
            [[]],
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]],
        )[0]

        distances = results.get(
            "distances",
            [[]],
        )[0]

        output = []

        for index, document in enumerate(documents):
            output.append(
                {
                    "document": document,
                    "metadata": (
                        metadatas[index]
                        if index < len(metadatas)
                        else {}
                    ),
                    "distance": (
                        distances[index]
                        if index < len(distances)
                        else None
                    ),
                }
            )

        return output

    def count(self) -> int:
        """
        Return number of stored chunks.
        """

        return self.collection.count()