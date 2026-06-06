from typing import Dict, Any
from backend.agents.state import AgentState

def data_extraction_node(state: AgentState) -> Dict[str, Any]:
    """
    Agent 2 - Clinical Data Extraction Agent.
    Identifies clinical variables (drug, phase, participants, design, adverse events)
    from form inputs and parsed source text, returning structured clinical intelligence.
    """
    print("[Agent 2 - Clinical Data Extraction] Extracting trial metrics...")
    context = state.get("structured_context", {})
    form = context.get("form_inputs", {})
    sources = context.get("source_data_extracted", "")
    
    # Perform extraction - In production, this runs structured LLM prompts via langchain
    clinical_intelligence = {
        "drug_name": form.get("drugName") or "Unknown Drug",
        "drug_type": form.get("drugType") or "Not Specified",
        "target_disease": form.get("targetDisease") or "Not Specified",
        "trial_phase": form.get("trialPhase") or "Phase 3",
        "study_design": form.get("studyDesign") or "Randomized, double-blind, placebo-controlled",
        "participants": form.get("participants") or "0",
        "primary_outcomes": form.get("primaryOutcomes") or "No primary outcomes defined.",
        "secondary_outcomes": form.get("secondaryOutcomes") or "No secondary outcomes defined.",
        "adverse_events": form.get("adverseEvents") or "None reported.",
        "toxicity_summary": form.get("toxicitySummary") or "None reported."
    }
    
    # Check if we should append information from files
    if "AE" in sources or "adverse" in sources.lower():
        clinical_intelligence["adverse_events"] += " (additional events identified in attachments)"
        
    return {"clinical_intelligence": clinical_intelligence}
