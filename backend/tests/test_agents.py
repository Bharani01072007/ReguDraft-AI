import pytest
from backend.agents.graph import agent_graph
from backend.agents.state import AgentState

def test_agent_graph_routing_csr():
    # Construct initial state with CSR type
    initial_state = {
        "project_id": "test-project-123",
        "document_id": "test-doc-123",
        "document_type": "CSR",
        "raw_inputs": {
            "drugName": "Aspirin",
            "trialPhase": "Phase 3",
            "studyDesign": "Double-blind, randomized",
        },
        "uploaded_file_urls": [],
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
    
    config = {"configurable": {"thread_id": "test-thread-csr"}}
    
    # Run graph till it interrupts
    events = agent_graph.stream(initial_state, config)
    final_state = initial_state
    for event in events:
        for val in event.values():
            final_state.update(val)
            
    # Assertions
    assert "Title Page" in final_state["draft_sections"]
    assert "Synopsis" in final_state["draft_sections"]
    assert "Efficacy Evaluation" in final_state["draft_sections"]
    assert "CLINICAL STUDY REPORT" in final_state["refined_draft"]
    assert final_state["compliance_report"]["compliance_score"] >= 90.0

def test_agent_graph_routing_ctd():
    initial_state = {
        "project_id": "test-project-123",
        "document_id": "test-doc-ctd",
        "document_type": "CTD",
        "raw_inputs": {
            "drugName": "Aspirin",
            "trialPhase": "Phase 1",
            "studyDesign": "Open-label",
        },
        "uploaded_file_urls": [],
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
    
    config = {"configurable": {"thread_id": "test-thread-ctd"}}
    events = agent_graph.stream(initial_state, config)
    final_state = initial_state
    for event in events:
        for val in event.values():
            final_state.update(val)
            
    assert "Module 1" in final_state["draft_sections"]
    assert "Module 2" in final_state["draft_sections"]
    assert "Module 5" in final_state["draft_sections"]
