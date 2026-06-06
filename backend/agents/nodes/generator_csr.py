from typing import Dict, Any
from backend.agents.state import AgentState

def generator_csr_node(state: AgentState) -> Dict[str, Any]:
    """
    Agent 5 - CSR Generation Agent.
    Drafts Clinical Study Reports conforming to ICH E3 guidelines.
    """
    print("[Agent 5 - CSR Generator] Drafting CSR sections (ICH E3)...")
    clinical = state.get("clinical_intelligence", {})
    reg_context = state.get("regulatory_context", {})
    
    draft_sections = {}
    
    draft_sections["Title Page"] = (
        f"# CLINICAL STUDY REPORT (CSR)\n\n"
        f"**DRUG PRODUCT:** {clinical.get('drug_name')}\n"
        f"**DRUG TYPE:** {clinical.get('drug_type')}\n"
        f"**INDICATION:** {clinical.get('target_disease')}\n"
        f"**TRIAL PHASE:** {clinical.get('trial_phase')}\n"
        f"**PROTOCOL STATUS:** Final\n"
    )
    
    draft_sections["Synopsis"] = (
        f"## Synopsis\n\n"
        f"This study was designed as a {clinical.get('study_design')} evaluating the therapeutic potential of {clinical.get('drug_name')} in subjects diagnosed with {clinical.get('target_disease')}.\n"
        f"A total of {clinical.get('participants')} participants were enrolled. The primary endpoints revolved around {clinical.get('primary_outcomes')}."
    )
    
    draft_sections["Introduction"] = (
        f"## Introduction & Study Objectives\n\n"
        f"Objectives of the study:\n"
        f"- Primary: {clinical.get('primary_outcomes')}\n"
        f"- Secondary: {clinical.get('secondary_outcomes')}\n"
    )
    
    draft_sections["Methodology"] = (
        f"## Methodology & Investigational Plan\n\n"
        f"The study protocol utilized a {clinical.get('study_design')} framework. "
        f"Participant inclusion criteria mapped strictly to diagnostic indices of {clinical.get('target_disease')}."
    )
    
    draft_sections["Efficacy Evaluation"] = (
        f"## Efficacy Evaluation\n\n"
        f"Primary Outcome Analysis:\n{clinical.get('primary_outcomes')}\n\n"
        f"Secondary Outcome Analysis:\n{clinical.get('secondary_outcomes')}\n"
    )
    
    draft_sections["Safety Evaluation"] = (
        f"## Safety Evaluation\n\n"
        f"Adverse events reported during the assessment period: {clinical.get('adverse_events')}.\n"
        f"Toxicity metrics summarized: {clinical.get('toxicity_summary')}."
    )
    
    draft_sections["Conclusion"] = (
        f"## Discussion & Conclusion\n\n"
        f"The efficacy analysis successfully addresses primary objectives. "
        f"Safety analysis shows an acceptable risk profile for {clinical.get('drug_name')} in treatment of {clinical.get('target_disease')}."
    )
    
    return {"draft_sections": draft_sections}
