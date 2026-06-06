import uuid
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database.session import get_db
from backend.database.models import Document, DocumentVersion, ComplianceReport, Export, UploadedFile, Project, User
from backend.schemas.documents import (
    DocumentCreate, DocumentResponse, DocumentDetailResponse, 
    UploadedFileResponse, ReviewSubmission, RefineRequest, RefineResponse,
    GenerateRequest
)
from backend.api.v1.dependencies import get_current_user
from backend.services.s3_service import s3_service
from backend.services.parser_service import parser_service
from backend.services import gemini_service, groq_service
from backend.agents.graph import agent_graph

router = APIRouter()


@router.post("/upload-file", response_model=UploadedFileResponse)
def upload_file(
    project_id: str = Form(...),
    document_id: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify project
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    # Upload to storage
    file_content = file.file.read()
    file_size = len(file_content)
    
    # Save to storage (local fallback or S3)
    object_name = f"projects/{project_id}/{uuid.uuid4()}_{file.filename}"
    file.file.seek(0)
    uploaded_url = s3_service.upload_fileobj(file.file, object_name)
    
    # Parse file contents
    extracted_text = parser_service.parse_file(file_content, file.filename)
    
    # Create DB model
    uploaded_file = UploadedFile(
        project_id=project_id,
        document_id=document_id,
        file_name=file.filename,
        file_url=uploaded_url,
        file_type=file.filename.split(".")[-1].lower(),
        file_size=file_size,
        extracted_text=extracted_text,
        uploaded_by=current_user.id
    )
    db.add(uploaded_file)
    db.commit()
    db.refresh(uploaded_file)
    return uploaded_file

@router.post("/{document_id}/generate")
def generate_draft(
    document_id: str, 
    req_body: Optional[GenerateRequest] = None,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Verify document
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        
    # Get associated upload files for context
    attached_files = db.query(UploadedFile).filter(UploadedFile.document_id == document_id).all()
    file_urls = [f.file_url for f in attached_files]
    
    # Construct initial state
    raw_inputs = {
        "drugName": doc.name.split("-")[-1].strip(),
        "trialPhase": "Phase 3",
        "studyDesign": "Double-blind, randomized",
    }
    if req_body and req_body.raw_inputs:
        raw_inputs.update(req_body.raw_inputs)
        
    initial_state = {
        "project_id": doc.project_id,
        "document_id": doc.id,
        "document_type": doc.type,
        "raw_inputs": raw_inputs,
        "uploaded_file_urls": file_urls,
        "structured_context": {},
        "clinical_intelligence": {},
        "regulatory_context": {},
        "draft_sections": {},
        "refined_draft": "",
        "compliance_report": {},
        "review_status": "PENDING",
        "review_comments": [],
        "export_urls": {},
        "errors": []
    }
    
    # Compile and execute the LangGraph workflow
    # LangGraph will halt at 'human_review' node because of interrupt_before=['human_review']
    config = {"configurable": {"thread_id": doc.id}}
    
    try:
        # Run graph. It will execute nodes 1-9 and then interrupt
        events = agent_graph.stream(initial_state, config)
        final_state = initial_state
        for event in events:
            # Aggregate updates to find final state before interrupt
            for val in event.values():
                final_state.update(val)
                
        # Create a new version for this document in the database
        version_count = db.query(DocumentVersion).filter(DocumentVersion.document_id == document_id).count()
        new_version_num = version_count + 1
        
        version = DocumentVersion(
            document_id=doc.id,
            version_number=new_version_num,
            content_markdown=final_state.get("refined_draft", "# Empty Draft"),
            change_summary="Initial AI generation draft",
            author_id=current_user.id
        )
        db.add(version)
        db.commit()
        db.refresh(version)
        
        # Save compliance report
        report_data = final_state.get("compliance_report", {})
        comp_report = ComplianceReport(
            version_id=version.id,
            compliance_score=report_data.get("compliance_score", 100.0),
            issues=report_data.get("issues", []),
            suggestions=report_data.get("suggestions", [])
        )
        db.add(comp_report)
        
        # Update current version reference in document
        doc.status = "IN_REVIEW"
        doc.current_version_id = version.id
        db.commit()
        
        return {
            "document_id": doc.id,
            "version_id": version.id,
            "status": doc.status,
            "compliance_score": comp_report.compliance_score,
            "message": "LangGraph execution suspended. Pending human review."
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent workflow generation failed: {str(e)}"
        )

@router.get("/{document_id}", response_model=DocumentDetailResponse)
def get_document(document_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        
    # Get current version and compliance report
    version = None
    report = None
    
    if doc.current_version_id:
        version = db.query(DocumentVersion).filter(DocumentVersion.id == doc.current_version_id).first()
        if version:
            report = db.query(ComplianceReport).filter(ComplianceReport.version_id == version.id).first()
            
    return {
        "id": doc.id,
        "project_id": doc.project_id,
        "name": doc.name,
        "type": doc.type,
        "status": doc.status,
        "current_version": version,
        "compliance_report": report
    }

@router.post("/{document_id}/submit-review")
def submit_review(document_id: str, review: ReviewSubmission, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        
    version = db.query(DocumentVersion).filter(DocumentVersion.id == doc.current_version_id).first()
    if not version:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document version not found")

    if review.action == "APPROVE":
        doc.status = "APPROVED"
        version.is_approved = True
        
        # Resume LangGraph with review state = APPROVED
        # This will trigger exporter_node
        try:
            config = {"configurable": {"thread_id": doc.id}}
            # 1. Update the state with approval data and comments
            agent_graph.update_state(config, {
                "review_status": "APPROVED",
                "review_comments": review.comments,
                "refined_draft": version.content_markdown,
                "document_id": doc.id
            })
            
            # 2. Resume graph execution from the breakpoint (pass None)
            events = agent_graph.stream(None, config)
            for event in events:
                pass  # Wait for workflow completion
                
            # 3. Retrieve the final state from the thread checkpointer
            final_state = agent_graph.get_state(config).values
            
            # Save export entries in DB
            for fmt, url in final_state.get("export_urls", {}).items():
                exp = Export(
                    version_id=version.id,
                    format=fmt,
                    file_url=url
                )
                db.add(exp)
            
            doc.status = "EXPORTED"
            db.commit()
            
            return {
                "document_id": doc.id,
                "status": doc.status,
                "exports": final_state.get("export_urls", {}),
                "message": "Document approved and exported successfully."
            }
        except Exception as e:
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Resuming export workflow failed: {str(e)}"
            )
            
    elif review.action == "REJECT" or review.action == "EDIT":
        # Loop back to medical writer with comments
        doc.status = "DRAFT"
        version.is_approved = False
        
        if review.edited_content:
            version.content_markdown = review.edited_content
            version.change_summary = f"Human editor revisions: {', '.join(review.comments)}"
        else:
            version.change_summary = f"Rejected: {', '.join(review.comments)}"
            
        db.commit()
        return {
            "document_id": doc.id,
            "status": doc.status,
            "message": "Review response registered. Draft status returned to edit phase."
        }
        
    else:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid review action")


@router.post("/refine", response_model=RefineResponse)
def refine_document_content(
    req: RefineRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Perform inline AI updates (IMPROVE, SUMMARIZE, EXPAND) on editor markdown content using Groq or Gemini.
    """
    content = req.content
    action = req.action.upper()
    
    # Select active LLM service
    active_service = None
    service_name = ""
    if groq_service.api_key:
        active_service = groq_service
        service_name = "Groq"
    elif gemini_service.api_key:
        active_service = gemini_service
        service_name = "Gemini"

    import re
    def strip_markdown(text: str) -> str:
        if not text:
            return text
        # Remove images: ![alt](url) -> ""
        text = re.sub(r'!\[([^\]]*)\]\([^\)]*\)', '', text)
        # Remove links: [text](url) -> text
        text = re.sub(r'\[([^\]]*)\]\([^\)]*\)', r'\1', text)
        # Remove bold/italic markdown characters: **, *, __, _
        text = text.replace("**", "").replace("__", "")
        text = text.replace("*", "").replace("_", "")
        # Remove header markdown characters at the start of any line: #, ##, ###, etc.
        text = re.sub(r'^\s*#+\s*', '', text, flags=re.MULTILINE)
        # Remove list items: leading - or + or * followed by space
        text = re.sub(r'^\s*[-+*]\s+', '', text, flags=re.MULTILINE)
        # Remove horizontal rules: ---, ***, ___
        text = re.sub(r'^\s*[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
        # Remove blockquotes: leading >
        text = re.sub(r'^\s*>\s*', '', text, flags=re.MULTILINE)
        # Remove inline code blocks: `text` -> text
        text = re.sub(r'`([^`]*)`', r'\1', text)
        return text


    if not active_service:
        print("[AI Editor Tool] No LLM API key configured. Returning basic mock response.")
        if action == "IMPROVE":
            return {"refined_content": strip_markdown(content + "\n\n* AI Note: This section was polished (mock). *")}
        elif action == "SUMMARIZE":
            return {"refined_content": strip_markdown("### Summary\nThis section summarizes the preceding content.")}
        elif action == "EXPAND":
            return {"refined_content": strip_markdown(content + "\n\nThis is additional detail expanded by the AI model.")}
        return {"refined_content": strip_markdown(content)}
        
    print(f"[AI Editor Tool] Running action {action} using {service_name}...")

    if action == "IMPROVE":
        prompt = (
            f"You are a regulatory medical writing assistant. Improve the writing quality of the following draft segment. "
            f"Enforce clear, concise, and professional scientific phrasing suitable for FDA submission. "
            f"Return only the improved text block, no introduction or other chat:\n\n{content}"
        )
    elif action == "SUMMARIZE":
        prompt = (
            f"You are a regulatory medical writing assistant. Summarize the following document segment into a concise summary subsection. "
            f"Enforce standard professional clinical overview tone. "
            f"Return only the summary markdown block, no introduction or other chat:\n\n{content}"
        )
    elif action == "EXPAND":
        prompt = (
            f"You are a regulatory medical writing assistant. Expand on the explanation of the following segment. "
            f"Elaborate on details, methodologies, and outcomes contextually based on standard medical literature templates. "
            f"Return only the expanded markdown block, no introduction or other chat:\n\n{content}"
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid refinement action")
        
    system_instruction = "You are an expert regulatory affairs writer."
    refined = active_service.generate_text(prompt, system_instruction)
    
    if refined.startswith("[Error:"):
        raise HTTPException(status_code=502, detail=refined)
        
    return {"refined_content": strip_markdown(refined)}

