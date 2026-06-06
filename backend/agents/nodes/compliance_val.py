from typing import Dict, Any, List
from backend.agents.state import AgentState

def compliance_val_node(state: AgentState) -> Dict[str, Any]:
    """
    Agent 9 - Compliance Validation Agent.
    Validates structural integrity, checks for placeholders, calculates
    a numeric compliance score, and logs warnings/suggestions.
    """
    print("[Agent 9 - Compliance Validation] Scanning draft for structural alignment...")
    draft = state.get("refined_draft", "")
    doc_type = state.get("document_type", "CSR")
    
    issues = []
    suggestions = []
    score = 100.0
    
    # Check for placeholder markers
    placeholders = ["[Drug Name]", "[N]", "[X]", "Unknown", "Not Specified"]
    found_placeholders = [p for p in placeholders if p in draft]
    
    if found_placeholders:
        score -= (len(found_placeholders) * 5.0)
        issues.append({
            "severity": "WARNING",
            "section": "General",
            "message": f"Contains unpopulated placeholder tags: {', '.join(found_placeholders)}."
        })
        suggestions.append({
            "section": "General",
            "message": "Replace placeholder fields with clinical parameters before final export."
        })
        
    # Check document type requirements
    if doc_type == "CSR":
        if "Synopsis" not in draft:
            score -= 15.0
            issues.append({
                "severity": "ERROR",
                "section": "Synopsis",
                "message": "Required ICH E3 Synopsis section is missing."
            })
        if "Safety" not in draft:
            score -= 20.0
            issues.append({
                "severity": "ERROR",
                "section": "Safety Evaluation",
                "message": "Safety evaluation data section is missing."
            })
            
    # Bound the score
    score = max(0.0, min(100.0, score))
    
    compliance_report = {
        "compliance_score": score,
        "issues": issues,
        "suggestions": suggestions
    }
    
    return {"compliance_report": compliance_report}
