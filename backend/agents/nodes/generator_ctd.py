from typing import Dict, Any
from backend.agents.state import AgentState

def generator_ctd_node(state: AgentState) -> Dict[str, Any]:
    """
    Agent 6 - CTD Generation Agent.
    Drafts Common Technical Document modules according to ICH M4.
    """
    print("[Agent 6 - CTD Generator] Drafting CTD modules (ICH M4)...")
    clinical = state.get("clinical_intelligence", {})
    
    draft_sections = {}
    
    draft_sections["Module 1"] = (
        f"# COMMON TECHNICAL DOCUMENT (CTD)\n\n"
        f"## Module 1: Administrative Information\n\n"
        f"**Applicant:** ReguDraft Therapeutics Inc.\n"
        f"**Product Name:** {clinical.get('drug_name')}\n"
        f"**Proposed Indication:** Treatment of {clinical.get('target_disease')}\n"
    )
    
    draft_sections["Module 2"] = (
        f"## Module 2: CTD Summaries\n\n"
        f"### Clinical Overview\n"
        f"The active substance is {clinical.get('drug_name')}, a {clinical.get('drug_type')} designed for the treatment of {clinical.get('target_disease')}.\n"
        f"In clinical tests comprising {clinical.get('participants')} subjects, the primary outcome profile revealed: {clinical.get('primary_outcomes')}"
    )
    
    draft_sections["Module 3"] = (
        f"## Module 3: Quality\n\n"
        f"Chemical, pharmaceutical, and biological documentation for {clinical.get('drug_name')}. "
        f"Structure elucidation and control of impurities align with FDA regulations for drug class: {clinical.get('drug_type')}."
    )
    
    draft_sections["Module 4"] = (
        f"## Module 4: Nonclinical Study Reports\n\n"
        f"Pharmacological indices support the dosing schema. The toxicity limits are detailed as: {clinical.get('toxicity_summary')}."
    )
    
    draft_sections["Module 5"] = (
        f"## Module 5: Clinical Study Reports\n\n"
        f"This module links to full reports from trials testing {clinical.get('drug_name')} in {clinical.get('target_disease')}. "
        f"Design profile: {clinical.get('study_design')}. Adverse reports: {clinical.get('adverse_events')}."
    )
    
    return {"draft_sections": draft_sections}
