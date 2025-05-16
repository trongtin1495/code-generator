from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any

class ProjectState(TypedDict):
    json_spec: Dict[str, Any]
    structure_plan: Dict[str, Any]
    generated_files: Dict[str, str]
    status: str

def build_project_graph():
    builder = StateGraph(ProjectState)

    # Add nodes and logic as before
    from agents.ios_structure_planner_agent import plan_structure
    from agents.code_generator_agent import generate_code
    from agents.project_assembler_agent import assemble_project
    from agents.ci_docs_agent import generate_ci_and_docs

    builder.add_node("PLAN_STRUCTURE", plan_structure)
    builder.add_node("GENERATE_CODE", generate_code)
    builder.add_node("ASSEMBLE_PROJECT", assemble_project)
    builder.add_node("CI_DOCS", generate_ci_and_docs)

    builder.set_entry_point("PLAN_STRUCTURE")

    builder.add_edge("PLAN_STRUCTURE", "GENERATE_CODE")
    builder.add_edge("GENERATE_CODE", "ASSEMBLE_PROJECT")
    builder.add_edge("ASSEMBLE_PROJECT", "CI_DOCS")
    builder.add_edge("CI_DOCS", END)

    return builder.compile()