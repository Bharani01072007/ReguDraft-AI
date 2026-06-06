from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from backend.schemas.knowledge import KnowledgeSearchRequest, KnowledgeSearchResponse
from backend.services.rag_service import rag_service
from backend.api.v1.dependencies import get_current_user, require_role
from backend.database.models.users import User

router = APIRouter()

@router.post("/search", response_model=KnowledgeSearchResponse)
def search_knowledge(
    req: KnowledgeSearchRequest, 
    current_user: User = Depends(get_current_user)
):
    """
    Search vector database for regulatory standards, guidelines, or checklists.
    """
    results = rag_service.search_guidelines(
        query=req.query,
        document_type=req.document_type,
        limit=req.limit
    )
    return {"results": results}

@router.post("/ingest", status_code=status.HTTP_201_CREATED)
def ingest_rule(
    text: str, 
    guideline_type: str, 
    document_type: str, 
    section_code: str,
    current_user: User = Depends(require_role(["ADMIN"]))
):
    """
    Manually insert a rule or template chunk. Restricted to ADMIN users.
    """
    metadata = {
        "guideline_type": guideline_type,
        "document_type": document_type,
        "section_code": section_code
    }
    success = rag_service.ingest_guideline(text, metadata)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to index knowledge item in vector store."
        )
    return {"status": "success", "message": "Knowledge chunk ingested successfully."}
