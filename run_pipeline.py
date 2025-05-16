# run_pipeline.py
import os
import argparse
from dotenv import load_dotenv

from core.figma_fetcher import download_figma_file
from core.figma_analyzer import analyze_and_save
from core.markdown_generator import generate_spec
from crew_runner import run_codegen_pipeline

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="End-to-end Figma to iOS code generator")
    parser.add_argument("--figma-key", required=True, help="Figma file key")
    parser.add_argument("--output-dir", default="./output", help="Directory to save all output files")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    figma_json = os.path.join(args.output_dir, "figma_design.json")
    summary_json = os.path.join(args.output_dir, "summary_report.json")
    markdown_md = os.path.join(args.output_dir, "figma_markdown.md")

    # PHASE 1
    download_figma_file(args.figma_key, figma_json)
    analyze_and_save(figma_json, summary_json)
    generate_spec(summary_json, figma_json, markdown_md)

    # PHASE 2
    run_codegen_pipeline(markdown_md) 

if __name__ == "__main__":
    main()