from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class DocumentCreate(BaseModel):
    name: str
    type: str  # "CSR", "CTD", "IND"
    raw_inputs: Dict[str, Any] = Field(default_factory=dict)

class DocumentResponse(BaseModel):
    id: str
    project_id: str
    name: str
    type: str
    status: str
    current_version_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DocumentVersionResponse(BaseModel):
    id: str
    document_id: str
    version_number: int
    content_markdown: str
    change_summary: Optional[str] = None
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ComplianceIssue(BaseModel):
    severity: str  # "WARNING", "ERROR", "INFO"
    section: str
    message: str

class ComplianceSuggestion(BaseModel):
    section: str
    message: str

class ComplianceReportResponse(BaseModel):
    compliance_score: float
    issues: List[ComplianceIssue] = Field(default_factory=list)
    suggestions: List[ComplianceSuggestion] = Field(default_factory=list)

    class Config:
        from_attributes = True

class DocumentDetailResponse(BaseModel):
    id: str
    project_id: str
    name: str
    type: str
    status: str
    current_version: Optional[DocumentVersionResponse] = None
    compliance_report: Optional[ComplianceReportResponse] = None

    class Config:
        from_attributes = True

class UploadedFileResponse(BaseModel):
    id: str
    project_id: str
    document_id: Optional[str] = None
    file_name: str
    file_url: str
    file_type: str
    file_size: int
    created_at: datetime

    class Config:
        from_attributes = True

class ReviewSubmission(BaseModel):
    action: str  # "APPROVE", "REJECT", "EDIT"
    edited_content: Optional[str] = None
    comments: List[str] = Field(default_factory=list)

class RefineRequest(BaseModel):
    content: str
    action: str  # "IMPROVE", "SUMMARIZE", "EXPAND"

class RefineResponse(BaseModel):
    refined_content: str

class GenerateRequest(BaseModel):
    raw_inputs: Optional[Dict[str, Any]] = None

