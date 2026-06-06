import uuid
from typing import Dict, Any
from backend.agents.state import AgentState
from backend.services.export_service import export_service
from backend.services.s3_service import s3_service

def exporter_node(state: AgentState) -> Dict[str, Any]:
    """
    Agent 11 - Document Export Agent.
    Converts final markdown draft into PDF, DOCX, and TXT,
    uploads them to object storage, and updates download endpoints.
    """
    print("[Agent 11 - Document Exporter] Generating final distribution files...")
    draft = state.get("refined_draft", "")
    doc_id = state.get("document_id", str(uuid.uuid4()))
    
    export_urls = {}
    
    # 1. Export as DOCX
    docx_bytes = export_service.export_to_docx(draft)
    docx_url = s3_service.upload_bytes(docx_bytes, f"exports/{doc_id}_final.docx")
    export_urls["docx"] = doc_url = docx_url

    # 2. Export as PDF
    pdf_bytes = export_service.export_to_pdf(draft)
    pdf_url = s3_service.upload_bytes(pdf_bytes, f"exports/{doc_id}_final.pdf")
    export_urls["pdf"] = pdf_url

    # 3. Export as TXT
    txt_bytes = export_service.export_to_txt(draft)
    txt_url = s3_service.upload_bytes(txt_bytes, f"exports/{doc_id}_final.txt")
    export_urls["txt"] = txt_url
    
    # 4. Save raw MD
    md_url = s3_service.upload_bytes(draft.encode("utf-8"), f"exports/{doc_id}_final.md")
    export_urls["md"] = md_url
    
    return {"export_urls": export_urls}
