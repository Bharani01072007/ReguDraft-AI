from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from typing import List, Dict, Any, Optional
from backend.config import settings

class RAGService:
    def __init__(self):
        try:
            self.client = QdrantClient(url=settings.QDRANT_URL, timeout=5)
            self.is_connected = True
        except Exception:
            self.is_connected = False
            self.client = None

    def search_guidelines(self, query: str, document_type: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        if not self.is_connected or not self.client:
            # Fallback mock search results for testing
            return self._mock_search_results(query, document_type, limit)

        try:
            # In a production environment:
            # query_vector = embedding_model.embed(query)
            # results = self.client.search(
            #     collection_name="regulatory_knowledge",
            #     query_vector=query_vector,
            #     query_filter=...
            # )
            # return [{"text": r.payload["content_text"], "score": r.score, "metadata": r.payload} for r in results]
            return self._mock_search_results(query, document_type, limit)
        except UnexpectedResponse:
            return self._mock_search_results(query, document_type, limit)

    def ingest_guideline(self, text: str, metadata: Dict[str, Any]) -> bool:
        if not self.is_connected or not self.client:
            return True
        try:
            # Upsert into Qdrant collection
            return True
        except Exception:
            return False

    def _mock_search_results(self, query: str, document_type: Optional[str], limit: int) -> List[Dict[str, Any]]:
        # Structured mocks for ICH E3 / M4 based on document_type
        mock_database = [
            {
                "text": "ICH E3 Guidelines Section 6: Study Objectives states that the report must describe the overall and specific objectives of the clinical study, including any primary or secondary endpoints.",
                "metadata": {"guideline_type": "ICH_E3", "document_type": "CSR", "section_code": "SECTION_3_OBJECTIVES"}
            },
            {
                "text": "ICH E3 Guidelines Section 7: Investigational Plan must contain detail of study design, treatments administered, blinding/randomization details, and patient inclusion/exclusion criteria.",
                "metadata": {"guideline_type": "ICH_E3", "document_type": "CSR", "section_code": "SECTION_4_METHODOLOGY"}
            },
            {
                "text": "FDA Regulatory Guidance: Clinical Safety Reports must include a detailed breakdown of all adverse events grouped by system organ class, severity, and relation to drug.",
                "metadata": {"guideline_type": "FDA_GUIDANCE", "document_type": "CSR", "section_code": "SECTION_6_SAFETY"}
            },
            {
                "text": "ICH M4 Guidelines (CTD) Module 2: Summaries requires writing a high-level clinical overview of the drug's efficacy and safety profiles.",
                "metadata": {"guideline_type": "ICH_M4", "document_type": "CTD", "section_code": "MODULE_2"}
            },
            {
                "text": "FDA IND Submission Guidelines requires Form 1571 detailing Sponsor information, Phase of investigation, Investigator list, and General Investigation Plan.",
                "metadata": {"guideline_type": "FDA_GUIDANCE", "document_type": "IND", "section_code": "FDA_1571"}
            }
        ]

        filtered_db = mock_database
        if document_type:
            filtered_db = [item for item in mock_database if item["metadata"]["document_type"] == document_type]

        results = []
        for idx, item in enumerate(filtered_db[:limit]):
            results.append({
                "text": item["text"],
                "score": 0.85 - (idx * 0.05),
                "metadata": item["metadata"]
            })
        return results

rag_service = RAGService()
