from pathlib import Path

import chromadb


class RAGService:
    """
    Local retrieval service for DroneRescue operational knowledge.
    """

    DOCUMENT_CATEGORIES = {
        "fire_protocol": "fire",
        "drone_safety": "general_safety",
        "emergency_response": "general_emergency",
        "battery_policy": "battery",
        "security_protocol": "security",
    }

    def __init__(
        self,
        knowledge_base_dir: str = "knowledge_base",
    ):
        self.knowledge_base_dir = Path(knowledge_base_dir)

        self.client = chromadb.PersistentClient(
            path="backend/rag/chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="drone_rescue_knowledge"
        )

    def ingest_documents(self) -> int:
        """
        Load all text documents from the knowledge base
        into the local ChromaDB collection.
        """

        documents = list(
            self.knowledge_base_dir.glob("*.txt")
        )

        if not documents:
            return 0

        for document_path in documents:
            text = document_path.read_text(
                encoding="utf-8"
            )

            category = self.DOCUMENT_CATEGORIES.get(
                document_path.stem,
                "general",
            )

            self.collection.upsert(
                ids=[document_path.stem],
                documents=[text],
                metadatas=[
                    {
                        "source": document_path.name,
                        "category": category,
                    }
                ],
            )

        return len(documents)

    def search(
        self,
        query: str,
        top_k: int = 3,
        category: str | None = None,
    ) -> list[dict]:
        """
        Retrieve the most relevant operational documents.

        If a category is provided, retrieval is restricted
        to documents belonging to that category.
        """

        query_kwargs = {
            "query_texts": [query],
            "n_results": top_k,
        }

        if category:
            query_kwargs["where"] = {
                "category": category,
            }

        results = self.collection.query(
            **query_kwargs
        )

        matches = []

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

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            matches.append(
                {
                    "document": document,
                    "source": metadata["source"],
                    "category": metadata["category"],
                    "distance": distance,
                }
            )

        return matches