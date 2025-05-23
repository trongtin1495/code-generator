import os
import re

def extract_file_blocks(content):
    """
    Extracts code blocks from the AI response in the format:
    --- file: <relative_path>
    <code>
    """
    pattern = r"--- file: (.+?)\n(.*?)(?=(?:--- file: )|$)"
    matches = re.findall(pattern, content, re.DOTALL)
    return [(filename.strip(), code.strip()) for filename, code in matches]

def assemble_project(state):
    print("📦 [ASSEMBLE_PROJECT] Writing generated files to disk...")
    output_dir = os.getenv("PROJECT_GENERATED_PATH", "./output/generated-project")
    os.makedirs(output_dir, exist_ok=True)

    files = state["generated_files"]

    for screen, content in files.items():
        print(f"✅ [ASSEMBLE_PROJECT] Wrote files for screen: {screen}")
        file_blocks = extract_file_blocks(content)
        for rel_path, code in file_blocks:
            abs_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "w") as f:
                f.write(code if code.startswith("//") else "// Generated by AI\n\n" + code)

    return {"status": "assembled"}