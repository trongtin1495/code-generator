import os
import json
from dotenv import load_dotenv
from agents.spec_to_json_agent import markdown_to_json
from dag_flow import build_project_graph

def run_codegen_pipeline(markdown_path: str):
    load_dotenv()

    # Load Markdown file
    with open(markdown_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    print("📄 Loaded Markdown spec:")
    print(markdown[:300] + "...\n")

    # Convert to JSON spec using AI agent
    json_spec = markdown_to_json(markdown)
    try:
        parsed_json = json.loads(json_spec)
    except json.JSONDecodeError as e:
        print("❌ LLM returned invalid JSON:\n", json_spec)
        raise e

    print("✅ Parsed JSON structure:")
    print(json.dumps(parsed_json, indent=2))

    # Run LangGraph pipeline
    print("\n🔁 Running LangGraph DAG to generate the project...\n")
    workflow = build_project_graph()
    workflow.invoke(input={"json_spec": parsed_json})
    print("🏁 Code generation complete.")

# Tests for run_codegen_pipeline
if __name__ == "__main__":
    test_path = "output/figma_markdown.md"
    if os.path.exists(test_path):
        print("🧪 Running codegen test on:", test_path)
        run_codegen_pipeline(test_path)
    else:
        print("❌ Test markdown file not found at:", test_path)