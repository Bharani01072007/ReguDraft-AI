from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    project_id: str
    document_id: str
    document_type: str                   # "CSR", "CTD", "IND"
    raw_inputs: Dict[str, Any]           # Client form text inputs
    uploaded_file_urls: List[str]        # List of S3 resource links
    
    # Processed states
    structured_context: Dict[str, Any]   # Text extracts & parsed parameters
    clinical_intelligence: Dict[str, Any]# Patient & Trial attributes
    regulatory_context: Dict[str, Any]    # Retrieved guidelines from Qdrant
    
    # Drafting contents
    draft_sections: Dict[str, str]       # Segment-specific drafted files
    refined_draft: str                   # Combined polishes from writer
    
    # Compliance & Review
    compliance_report: Dict[str, Any]    # Scoring issues lists
    review_status: str                   # "PENDING", "APPROVED", "REJECTED"
    review_comments: List[str]           # Revision feedback
    
    # Output file links
    export_urls: Dict[str, str]          # Formats -> download URLs
    errors: List[str]
