import json
import os
import requests
import time
import openai
from core.figma_analyzer import load_figma_json

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL = 'llama3'
MAX_CONTEXT_LENGTH = 12000
RETRY_LIMIT = 3

PROMPT_TEMPLATE = """
You are a senior product designer and business analyst. Your job is to write a single, professional, consolidated Markdown specification for mobile engineers and business stakeholders, based on a full set of Figma screen frames exported as JSON.

**Your output MUST:**
- Follow the exact structure, formatting, and level of detail as the sample below.
- Be clear, concise, and professional, suitable for direct handoff to developers and analysts.
- Use tables for color tokens, font styles, and navigation logic.
- List all screens in a single "Screen List" section, using numbered subsections.
- Summarize layout system, constraints, and business logic in dedicated sections.
- Exclude any status bar or system UI components (battery, wifi, signal, etc).
- Do NOT repeat section headers per screen.
- Do NOT include any placeholder text, apologies, or explanations.
- If information is missing, write "Not specified".
- Only output the Markdown document, nothing else.

**Sample structure:**

# 🎨 Design Page - Detailed Developer & Analyst Specification

## 📄 Overview
[Short summary of the app design and its purpose.]

---

### 1. [Screen Name]
- **Size:** [width] x [height] px
- **Background:** [Color name/code]
- **Components:**
  - [Component 1: description]
  - [Component 2: description]
- **Interaction:**
  - **Trigger:** [e.g. Button tap, timeout]
  - **Action:** [e.g. Navigate to X, Smart Animate]

---

## 📀 Layout System & Constraints
- **Corner Radius:** [value]
- **Grid:** [columns, margin, gutter]
- **Alignment:** [description]
- **Typography Grid:** [description]

---

## 🖍️ Color Tokens

| Purpose        | Color Name    | HEX       |
|----------------|---------------|-----------|
| Primary CTA    | Orange        | #FFA451   |
| Background     | White         | #FFFFFF   |
| ...            | ...           | ...       |

---

## 🌤️ Font Styles

| Usage       | Font Name     | Weight | Size  |
|-------------|---------------|--------|-------|
| Headings    | Stolzl Medium | 500    | 64pt  |
| ...         | ...           | ...    | ...   |

---

## 🔁 Navigation Logic

| From               | Trigger              | To                    | Transition        |
|--------------------|----------------------|-----------------------|-------------------|
| Splash Screen      | After 0.1s timeout   | Welcome Screen        | Smart Animate     |
| ...                | ...                  | ...                   | ...               |

---

**Now, using the provided Figma JSON, generate the full Markdown specification in this format.**
"""

def call_ollama(screen_name, screen_data):
    raw_json = json.dumps(screen_data, indent=2, ensure_ascii=False)
    if len(raw_json) > MAX_CONTEXT_LENGTH:
        raw_json = raw_json[:MAX_CONTEXT_LENGTH]

    payload = {
        "model": MODEL,
        "prompt": f"{PROMPT_TEMPLATE}\n\nScreen Name: {screen_name}\n\nFigma JSON:\n{raw_json}",
        "stream": True,
        "temperature": 0.2,
        "max_tokens": 4000
    }

    for attempt in range(RETRY_LIMIT):
        try:
            response = requests.post(OLLAMA_URL, json=payload, stream=True)
            if response.status_code != 200:
                raise Exception(f"Unexpected response status: {response.status_code} - {response.text}")
            markdown_output = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode("utf-8"))
                    chunk = data.get("response", "")
                    markdown_output += chunk
            return markdown_output
        except Exception as e:
            print(f"⚠️ Error calling Ollama (attempt {attempt+1}/{RETRY_LIMIT}): {type(e).__name__} - {e}")
            time.sleep(2)
    raise RuntimeError("❌ Failed to connect to Ollama model after multiple attempts. Please ensure the Ollama server is running and accessible.")

def call_openai(screen_name, screen_data):
    raw_json = json.dumps(screen_data, indent=2, ensure_ascii=False)
    if len(raw_json) > MAX_CONTEXT_LENGTH:
        raw_json = raw_json[:MAX_CONTEXT_LENGTH]

    prompt = f"{PROMPT_TEMPLATE}\n\nScreen Name: {screen_name}\n\nFigma JSON:\n{raw_json}"

    for attempt in range(RETRY_LIMIT):
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a senior product designer and business analyst. Your job is to write a single, professional, consolidated Markdown specification for mobile engineers and business stakeholders, based on a full set of Figma screen frames exported as JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=4000,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ Error calling OpenAI (attempt {attempt+1}/{RETRY_LIMIT}): {type(e).__name__} - {e}")
            time.sleep(2)
    raise RuntimeError("❌ Failed to connect to OpenAI model after multiple attempts. Please ensure your API key is valid and you have network access.")

def generate_spec(summary_path, figma_path, markdown_path):
    print("🛠 Generating Markdown spec from Figma summary...")

    # Load summary
    summary = load_figma_json(summary_path)
    valid_screens = set()

    # Dynamically select the first design page
    page_names = list(summary.get("pages", {}).keys())
    if not page_names:
        print("❌ No valid pages found in summary report.")
        return

    selected_page_name = page_names[0]
    page_data = summary["pages"].get(selected_page_name)

    if not page_data:
        print(f"❌ Page '{selected_page_name}' not found in summary.")
        return

    for screen in page_data.get("screens", []):
        if screen.get("name"):
            valid_screens.add(screen["name"])

    # Load figma full JSON
    figma_data = load_figma_json(figma_path)
    all_frames = []
    for page in figma_data.get("document", {}).get("children", []):
        if page.get("type") == "CANVAS" and page.get("name", "").strip() == selected_page_name:
            for node in page.get("children", []):
                if node.get("type") == "FRAME" and node.get("name") in valid_screens:
                    all_frames.append((page.get("name"), node))

    combined_output = ""
    for idx, (page_name, node) in enumerate(all_frames, start=1):
        screen_name = f"{page_name} - {node['name']}"
        print(f"🔄 Processing {screen_name}...")
        try:
            markdown = call_openai(screen_name, node)
            combined_output += f"\n\n{markdown.strip()}\n\n"
        except RuntimeError as err:
            print(f"❌ {err}")
            break
        time.sleep(1)

    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(combined_output.strip())
    print(f"✅ Markdown spec saved to: {markdown_path}")