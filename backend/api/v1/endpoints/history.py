import difflib
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database.session import get_db
from backend.database.models import Document, DocumentVersion, User
from backend.schemas.documents import DocumentVersionResponse
from backend.api.v1.dependencies import get_current_user

router = APIRouter()

@router.get("/{document_id}/versions", response_model=List[DocumentVersionResponse])
def get_document_versions(
    document_id: str, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Verify document exists
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        
    return db.query(DocumentVersion).filter(DocumentVersion.document_id == document_id).order_by(DocumentVersion.version_number.desc()).all()

@router.get("/versions/{version_id}", response_model=DocumentVersionResponse)
def get_version(
    version_id: str, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    version = db.query(DocumentVersion).filter(DocumentVersion.id == version_id).first()
    if not version:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Version not found")
    return version

@router.get("/versions/{version_id}/diff")
def get_version_diff(
    version_id: str, 
    compare_with_id: str, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    v1 = db.query(DocumentVersion).filter(DocumentVersion.id == version_id).first()
    v2 = db.query(DocumentVersion).filter(DocumentVersion.id == compare_with_id).first()
    
    if not v1 or not v2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or both versions not found")
        
    v1_lines = v1.content_markdown.splitlines()
    v2_lines = v2.content_markdown.splitlines()
    
    diff = difflib.unified_diff(
        v2_lines, 
        v1_lines, 
        fromfile=f"v{v2.version_number}", 
        tofile=f"v{v1.version_number}", 
        lineterm=""
    )
    
    return {
        "version_id": version_id,
        "compare_with_id": compare_with_id,
        "diff": list(diff)
    }
