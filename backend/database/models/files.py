import uuid
from sqlalchemy import Column, String, Text, Integer, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.base import Base

class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(1024), nullable=False)
    file_type = Column(String(50), nullable=False)  # "pdf", "docx", "txt"
    file_size = Column(Integer, nullable=False)
    extracted_text = Column(Text, nullable=True)
    file_metadata = Column(JSON, nullable=True)
    uploaded_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    project = relationship("Project", backref="uploaded_files")
    document = relationship("Document", backref="uploaded_files")
    uploader = relationship("User", backref="uploaded_files")
