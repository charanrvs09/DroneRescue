from backend.rag.rag_service import RAGService


class KnowledgeAgent:
    """
    Retrieves operational procedures relevant to an incident.
    """

    INCIDENT_CATEGORIES = {
        "fire": "fire",
        "security": "security",
        "intrusion": "security",
        "chemical_leak": "general_emergency",
        "accident": "general_emergency",
        "structural_damage": "general_emergency",
        "flooding": "general_emergency",
    }

    def __init__(self):
        self.rag = RAGService()

    def get_guidance(
        self,
        incident_type: str,
        query: str | None = None,
    ) -> dict:
        if query is None:
            query = (
                f"What are the operational procedures "
                f"for responding to a {incident_type} incident?"
            )

        category = self.INCIDENT_CATEGORIES.get(
            incident_type,
            "general_emergency",
        )

        results = self.rag.search(
            query,
            top_k=3,
            category=category,
        )

        guidance = []

        for result in results:
            guidance.append(
                {
                    "source": result["source"],
                    "content": result["document"],
                    "category": result["category"],
                    "distance": result["distance"],
                }
            )

        return {
            "incident_type": incident_type,
            "query": query,
            "category": category,
            "guidance": guidance,
        }