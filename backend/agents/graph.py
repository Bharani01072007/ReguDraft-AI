from langgraph.graph import StateGraph, END
from backend.agents.state import AgentState

# Import node handlers
from backend.agents.nodes.input_processing import input_processing_node
from backend.agents.nodes.data_extraction import data_extraction_node
from backend.agents.nodes.knowledge_rag import knowledge_rag_node
from backend.agents.nodes.generator_csr import generator_csr_node
from backend.agents.nodes.generator_ctd import generator_ctd_node
from backend.agents.nodes.generator_ind import generator_ind_node
from backend.agents.nodes.medical_writer import medical_writer_node
from backend.agents.nodes.compliance_val import compliance_val_node
from backend.agents.nodes.human_review import human_review_node
from backend.agents.nodes.exporter import exporter_node

# 1. Initialize Graph
workflow = StateGraph(AgentState)

# 2. Add Nodes
workflow.add_node("input_processing", input_processing_node)
workflow.add_node("data_extraction", data_extraction_node)
workflow.add_node("knowledge_rag", knowledge_rag_node)
workflow.add_node("generator_csr", generator_csr_node)
workflow.add_node("generator_ctd", generator_ctd_node)
workflow.add_node("generator_ind", generator_ind_node)
workflow.add_node("medical_writer", medical_writer_node)
workflow.add_node("compliance_validation", compliance_val_node)
workflow.add_node("human_review", human_review_node)
workflow.add_node("exporter", exporter_node)

# 3. Set entry point
workflow.set_entry_point("input_processing")

# 4. Standard edges
workflow.add_edge("input_processing", "data_extraction")
workflow.add_edge("data_extraction", "knowledge_rag")

# 5. Conditional Routing by Document Type
def route_by_document_type(state: AgentState) -> str:
    doc_type = state.get("document_type", "CSR").upper()
    if doc_type == "CSR":
        return "generator_csr"
    elif doc_type == "CTD":
        return "generator_ctd"
    elif doc_type == "IND":
        return "generator_ind"
    return "generator_csr"

workflow.add_conditional_edges(
    "knowledge_rag",
    route_by_document_type,
    {
        "generator_csr": "generator_csr",
        "generator_ctd": "generator_ctd",
        "generator_ind": "generator_ind"
    }
)

# 6. Reconnect generator paths to writer
workflow.add_edge("generator_csr", "medical_writer")
workflow.add_edge("generator_ctd", "medical_writer")
workflow.add_edge("generator_ind", "medical_writer")

# 7. Writer outputs to compliance checks
workflow.add_edge("medical_writer", "compliance_validation")
workflow.add_edge("compliance_validation", "human_review")

# 8. Conditional Routing by Human Review Status
def route_by_review_status(state: AgentState) -> str:
    status = state.get("review_status", "PENDING").upper()
    if status == "APPROVED":
        return "exporter"
    # If rejected or pending revisions, loop back to medical writer
    return "medical_writer"

workflow.add_conditional_edges(
    "human_review",
    route_by_review_status,
    {
        "exporter": "exporter",
        "medical_writer": "medical_writer"
    }
)

workflow.add_edge("exporter", END)

from langgraph.checkpoint.memory import MemorySaver

# 9. Compile Graph
# We specify interrupt_before=["human_review"] so that LangGraph halts automatically 
# before processing the review node, enabling asynchronous Human-In-The-Loop review.
memory = MemorySaver()
agent_graph = workflow.compile(
    checkpointer=memory,
    interrupt_before=["human_review"]
)
