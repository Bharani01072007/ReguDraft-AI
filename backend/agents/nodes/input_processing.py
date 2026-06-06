from typing import Dict, Any
from backend.agents.state import AgentState
from backend.services.parser_service import parser_service

def input_processing_node(state: AgentState) -> Dict[str, Any]:
    """
    Agent 1 - Input Processing Agent.
    Parses and cleans input files (PDF/DOCX/TXT), extracts basic file metadata, 
    and groups them with manual form data into a structured context.
    """
    print("[Agent 1 - Input Processing] Validating and parsing inputs...")
    raw_inputs = state.get("raw_inputs", {})
    uploaded_file_urls = state.get("uploaded_file_urls", [])
    
    extracted_texts = []
    
    # Simulating parsing of files downloaded from S3 or direct database fetch
    for url in uploaded_file_urls:
        filename = url.split("/")[-1]
        # Simulate loading file contents
        mock_content = f"Simulated document content of file: {filename}. Clinical data for drug {raw_inputs.get('drugName')}."
        parsed_text = parser_service.parse_file(mock_content.encode("utf-8"), filename)
        extracted_texts.append(f"Source file: {filename}\nContent:\n{parsed_text}")

    combined_sources = "\n\n---\n\n".join(extracted_texts)
    
    structured_context = {
        "form_inputs": raw_inputs,
        "parsed_files_count": len(uploaded_file_urls),
        "source_data_extracted": combined_sources if combined_sources else "No upload files provided."
    }
    
    return {"structured_context": structured_context}
