import re
from typing import Dict, Any
from backend.agents.state import AgentState
from backend.services import gemini_service, groq_service

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


def medical_writer_node(state: AgentState) -> Dict[str, Any]:
    """
    Agent 8 - Medical Writing Agent.
    Aggregates section drafts, enforces professional scientific transitions,
    and converts text to a formal regulatory style using Groq (or Gemini).
    """
    sections = state.get("draft_sections", {})
    clinical = state.get("clinical_intelligence", {})
    
    if not sections:
        return {"refined_draft": "# Generated Draft\n\nNo sections drafted."}
        
    combined_content = []
    
    # We combine the sections in an ordered logical sequence
    for sec_title, sec_content in sections.items():
        combined_content.append(sec_content)
        
    full_draft = "\n\n---\n\n".join(combined_content)
    
    # Select active LLM service
    active_service = None
    service_name = ""
    if groq_service.api_key:
        active_service = groq_service
        service_name = "Groq"
    elif gemini_service.api_key:
        active_service = gemini_service
        service_name = "Gemini"

    if not active_service:
        print("[Agent 8 - Medical Writer] No LLM API key provided. Using basic mock text substitutions.")
        # Fallback if no key is configured
        polished_draft = (
            full_draft
            .replace("efficacy analysis successfully addresses", "efficacy data demonstrated statistical significance in addressing")
            .replace("acceptable risk profile", "safety profile congruent with investigational requirements")
        )
        return {"refined_draft": strip_markdown(polished_draft)}
        
    print(f"[Agent 8 - Medical Writer] Polishing text to formal regulatory tone using {service_name}...")
    
    # Generate prompt for LLM
    prompt = (
        f"You are an expert regulatory medical writer. Review the following draft regulatory document and reframe it. "
        f"Enforce a highly professional, formal, scientific, and FDA-compliant tone. Resolve transitions between sections. "
        f"You must preserve all original section headers (such as 'Synopsis', 'Safety Evaluation', etc.) without renaming, removing, or omitting them. "
        f"Ensure no bracketed placeholders (like [Drug Name], [Target Disease], [N], etc.) remain; fill them in contextually using the clinical details below:\n\n"
        f"CLINICAL DETAILS:\n"
        f"- Drug Name: {clinical.get('drug_name')}\n"
        f"- Drug Type: {clinical.get('drug_type')}\n"
        f"- Disease: {clinical.get('target_disease')}\n"
        f"- Phase: {clinical.get('trial_phase')}\n"
        f"- Design: {clinical.get('study_design')}\n"
        f"- Participants: {clinical.get('participants')}\n"
        f"- Primary Outcomes: {clinical.get('primary_outcomes')}\n"
        f"- Secondary Outcomes: {clinical.get('secondary_outcomes')}\n"
        f"- Adverse Events: {clinical.get('adverse_events')}\n"
        f"- Toxicity: {clinical.get('toxicity_summary')}\n\n"
        f"RAW DRAFT:\n{full_draft}\n\n"
        f"Return the polished, final markdown document. Output only the markdown text, no other chat."
    )
    
    system_instruction = "You are a senior regulatory affairs medical writer generating reports for FDA submissions."
    
    polished_draft = active_service.generate_text(prompt, system_instruction)
    
    if polished_draft.startswith("[Error:"):
        print(f"[{service_name} Error in Writer]: {polished_draft}")
        # fallback to raw draft
        return {"refined_draft": strip_markdown(full_draft)}
        
    return {"refined_draft": strip_markdown(polished_draft)}

