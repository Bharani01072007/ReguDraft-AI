from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class KnowledgeSearchRequest(BaseModel):
    query: str
    document_type: Optional[str] = None  # "CSR", "CTD", "IND"
    limit: int = 5

class KnowledgeSearchResult(BaseModel):
    text: str
    score: float
    metadata: Dict[str, Any]

class KnowledgeSearchResponse(BaseModel):
    results: List[KnowledgeSearchResult]
