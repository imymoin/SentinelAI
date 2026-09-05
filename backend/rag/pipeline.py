from pathlib import Path

from backend.rag.chunker import chunk_text
from backend.rag.loader import load_document
from backend.rag.retriever import RAGRetriever
from backend.rag.vectorstore import ChromaVectorStore


class RAGPipeline:
    """
    End-to-end RAG pipeline.

    Document:
        Load → Chunk → Embed → ChromaDB

    Query:
        Query → Embed → ChromaDB → Context
    """

    def __init__(
        self,
        persist_directory: str = "data/chroma",
        collection_name: str = "sentinel_documents",
        top_k: int = 3,
    ):
        self.vector_store = ChromaVectorStore(
            persist_directory=persist_directory,
            collection_name=collection_name,
        )

        self.retriever = RAGRetriever(
            vector_store=self.vector_store,
            top_k=top_k,
        )

    def ingest_file(
        self,
        file_path: str,
    ) -> int:
        """
        Load and index a document.

        Returns:
            Number of chunks indexed.
        """

        text = load_document(file_path)

        chunks = chunk_text(text)

        if not chunks:
            return 0

        source = Path(file_path).name

        metadatas = [
            {
                "source": source,
                "chunk_index": index,
            }
            for index in range(len(chunks))
        ]

        ids = [
            f"{source}_{index}"
            for index in range(len(chunks))
        ]

        self.vector_store.add_documents(
            documents=chunks,
            metadatas=metadatas,
            ids=ids,
        )

        return len(chunks)

    def ingest_text(
        self,
        text: str,
        source: str = "manual",
    ) -> int:
        """
        Index raw text directly.
        """

        chunks = chunk_text(text)

        if not chunks:
            return 0

        metadatas = [
            {
                "source": source,
                "chunk_index": index,
            }
            for index in range(len(chunks))
        ]

        ids = [
            f"{source}_{index}"
            for index in range(len(chunks))
        ]

        self.vector_store.add_documents(
            documents=chunks,
            metadatas=metadatas,
            ids=ids,
        )

        return len(chunks)

    def retrieve(
        self,
        query: str,
    ) -> list[dict]:
        """
        Retrieve relevant chunks.
        """

        return self.retriever.retrieve(query)

    def get_context(
        self,
        query: str,
    ) -> str:
        """
        Get context suitable for an LLM prompt.
        """

        return self.retriever.get_context(query)

    def document_count(self) -> int:
        """
        Return number of indexed chunks.
        """

        return self.vector_store.count()