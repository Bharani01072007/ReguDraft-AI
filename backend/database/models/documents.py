import uuid
from sqlalchemy import Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.base import Base

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # "CSR", "CTD", "IND"
    status = Column(String(50), default="DRAFT", nullable=False)  # "DRAFT", "IN_REVIEW", "APPROVED", "EXPORTED"
    current_version_id = Column(String(36), nullable=True) # Point to a specific document_versions.id
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", backref="documents")
    versions = relationship("DocumentVersion", foreign_keys="[DocumentVersion.document_id]", back_populates="document", cascade="all, delete-orphan")

class DocumentVersion(Base):
    __tablename__ = "document_versions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    version_number = Column(Integer, nullable=False)
    content_markdown = Column(Text, nullable=False)
    author_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    change_summary = Column(Text, nullable=True)
    is_approved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    document = relationship("Document", foreign_keys=[document_id], back_populates="versions")
    author = relationship("User", backref="authored_versions")
    compliance_reports = relationship("ComplianceReport", back_populates="version", cascade="all, delete-orphan")
    exports = relationship("Export", back_populates="version", cascade="all, delete-orphan")

class ComplianceReport(Base):
    __tablename__ = "compliance_reports"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    version_id = Column(String(36), ForeignKey("document_versions.id", ondelete="CASCADE"), nullable=False)
    compliance_score = Column(Float, default=0.0, nullable=False)
    issues = Column(JSON, nullable=True)  # List of objects containing severity, section, message
    suggestions = Column(JSON, nullable=True)  # List of objects containing section, message
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    version = relationship("DocumentVersion", back_populates="compliance_reports")

class Export(Base):
    __tablename__ = "exports"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    version_id = Column(String(36), ForeignKey("document_versions.id", ondelete="CASCADE"), nullable=False)
    format = Column(String(20), nullable=False)  # "pdf", "docx", "txt", "md"
    file_url = Column(String(1024), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    version = relationship("DocumentVersion", back_populates="exports")
