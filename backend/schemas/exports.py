from pydantic import BaseModel
from datetime import datetime

class ExportCreate(BaseModel):
    format: str  # "pdf" | "docx" | "txt" | "md"
    theme_template: str = "modern_branded"

class ExportResponse(BaseModel):
    export_id: str
    version_id: str
    format: str
    file_url: str
    created_at: datetime
