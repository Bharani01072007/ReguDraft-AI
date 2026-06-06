import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.database.models import DocumentVersion, Export, User
from backend.schemas.exports import ExportCreate, ExportResponse
from backend.services.export_service import export_service
from backend.services.s3_service import s3_service
from backend.api.v1.dependencies import get_current_user

router = APIRouter()

@router.post("/versions/{version_id}/export", response_model=ExportResponse)
def export_document_version(
    version_id: str,
    req: ExportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    version = db.query(DocumentVersion).filter(DocumentVersion.id == version_id).first()
    if not version:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document version not found")
        
    markdown_content = version.content_markdown
    file_format = req.format.lower()
    
    # Generate requested file binary
    if file_format == "pdf":
        file_bytes = export_service.export_to_pdf(markdown_content)
    elif file_format == "docx":
        file_bytes = export_service.export_to_docx(markdown_content)
    elif file_format in ["txt", "md"]:
        file_bytes = export_service.export_to_txt(markdown_content)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported export format")
        
    # Upload to storage
    object_name = f"exports/{version.document_id}/{uuid.uuid4()}_version_{version.version_number}.{file_format}"
    file_url = s3_service.upload_bytes(file_bytes, object_name)
    
    # Write to Export DB
    export_entry = Export(
        version_id=version_id,
        format=file_format,
        file_url=file_url
    )
    db.add(export_entry)
    db.commit()
    db.refresh(export_entry)
    
    return {
        "export_id": export_entry.id,
        "version_id": version_id,
        "format": file_format,
        "file_url": file_url,
        "created_at": export_entry.created_at
    }
