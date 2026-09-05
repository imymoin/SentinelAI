from backend.rag.vectorstore import ChromaVectorStore


class RAGRetriever:
    """
    Retrieves relevant context from ChromaDB.
    """

    def __init__(
        self,
        vector_store: ChromaVectorStore | None = None,
        top_k: int = 3,
    ):
        self.vector_store = (
            vector_store
            if vector_store
            else ChromaVectorStore()
        )

        self.top_k = top_k

    def retrieve(
        self,
        query: str,
    ) -> list[dict]:
        """
        Retrieve relevant documents.
        """

        return self.vector_store.search(
            query=query,
            top_k=self.top_k,
        )

    def get_context(
        self,
        query: str,
    ) -> str:
        """
        Combine retrieved documents into context
        for the LLM.
        """

        results = self.retrieve(query)

        if not results:
            return ""

        context_parts = []

        for result in results:
            context_parts.append(
                result["document"]
            )

        return "\n\n---\n\n".join(
            context_parts
        )