from typing import Dict, Any
from backend.agents.state import AgentState

def generator_ind_node(state: AgentState) -> Dict[str, Any]:
    """
    Agent 7 - IND Generation Agent.
    Drafts FDA Investigational New Drug (IND) application sections.
    """
    print("[Agent 7 - IND Generator] Drafting IND submission templates...")
    clinical = state.get("clinical_intelligence", {})
    
    draft_sections = {}
    
    draft_sections["Cover Letter"] = (
        f"# INVESTIGATIONAL NEW DRUG APPLICATION (IND)\n\n"
        f"## Cover Letter\n\n"
        f"Food and Drug Administration\n"
        f"Center for Drug Evaluation and Research\n\n"
        f"Dear Director,\n\n"
        f"ReguDraft Therapeutics hereby submits an initial Investigational New Drug Application (IND) for {clinical.get('drug_name')}, "
        f"a new chemical entity intended for the treatment of {clinical.get('target_disease')}.\n"
    )
    
    draft_sections["FDA 1571 Information"] = (
        f"## Form FDA 1571 Summary\n\n"
        f"- **Sponsor:** ReguDraft Therapeutics Inc.\n"
        f"- **Name of Drug:** {clinical.get('drug_name')}\n"
        f"- **Phase of Investigation:** {clinical.get('trial_phase')}\n"
        f"- **Indication:** Treatment of {clinical.get('target_disease')}\n"
    )
    
    draft_sections["General Investigation Plan"] = (
        f"## General Investigation Plan\n\n"
        f"The primary focus of this investigation is to evaluate safety and clinical outcomes in Phase 1-3. "
        f"The anticipated study population contains approximately {clinical.get('participants')} subjects using a {clinical.get('study_design')} structure."
    )
    
    draft_sections["Toxicology Data"] = (
        f"## Toxicology & Pharmacology\n\n"
        f"Preclinical pharmacology evaluations establish starting dose guidelines. "
        f"Preclinical toxicological reviews summary: {clinical.get('toxicity_summary')}."
    )
    
    draft_sections["Manufacturing Information"] = (
        f"## Chemistry, Manufacturing, and Control (CMC)\n\n"
        f"Chemistry details for drug type: {clinical.get('drug_type')}. "
        f"Specifications, stability tests, and manufacturing flowcharts are logged in CMC files."
    )
    
    draft_sections["Clinical Protocols"] = (
        f"## Proposed Clinical Protocols\n\n"
        f"Protocol details:\n"
        f"- Primary Endpoints: {clinical.get('primary_outcomes')}\n"
        f"- Secondary Endpoints: {clinical.get('secondary_outcomes')}\n"
    )
    
    return {"draft_sections": draft_sections}
