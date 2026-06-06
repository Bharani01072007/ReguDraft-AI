from typing import Dict, Any
from backend.agents.state import AgentState
from backend.services.rag_service import rag_service

def knowledge_rag_node(state: AgentState) -> Dict[str, Any]:
    """
    Agent 3 - Regulatory Knowledge Agent.
    Performs vector similarity search against ICH E3/M4 templates and FDA guidelines,
    filtering by document type (CSR, CTD, IND) to build context.
    """
    print("[Agent 3 - Regulatory Knowledge RAG] Searching vector DB for guidelines...")
    doc_type = state.get("document_type", "CSR")
    clinical_intel = state.get("clinical_intelligence", {})
    
    # Formulate query based on drug and trial characteristics
    query = f"guidelines and requirements for drafting a {doc_type} report for a {clinical_intel.get('trial_phase')} {clinical_intel.get('study_design')} study"
    
    # Execute vector search
    search_hits = rag_service.search_guidelines(
        query=query, 
        document_type=doc_type, 
        limit=3
    )
    
    # Combine retrieved texts
    retrieved_guidelines = []
    for hit in search_hits:
        retrieved_guidelines.append({
            "text": hit["text"],
            "section": hit["metadata"].get("section_code"),
            "source": hit["metadata"].get("guideline_type")
        })
        
    regulatory_context = {
        "document_type": doc_type,
        "retrieved_guidelines": retrieved_guidelines,
        "guideline_mapping_applied": True
    }
    
    return {"regulatory_context": regulatory_context}
