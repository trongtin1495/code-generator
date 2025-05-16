import os

def generate_ci_and_docs(state):
    output_dir = os.getenv("PROJECT_GENERATED_PATH", "./output/generated-project")
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "README.md"), "w") as f:
        f.write("# Auto-Generated iOS App\n\nThis project was initialized via AI.\n")

    os.makedirs(os.path.join(output_dir, ".github", "workflows"), exist_ok=True)
    with open(os.path.join(output_dir, ".github", "workflows", "ci.yml"), "w") as f:
        f.write("""name: CI
on: [push]
jobs:
  build:
    runs-on: macos-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build
      run: echo 'Xcode build step here'
""")
    return {"status": "docs_and_ci_ready"}