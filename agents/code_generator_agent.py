from openai import OpenAI
import os

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_code(state):
    print("🧠 [GENERATE_CODE] Generating Swift UIKit + MVVM Clean Architecture files with AI...")
    structure = state["structure_plan"]
    screens = structure["screens"]

    swift_files = {}

    for screen in screens:
        screen_name = screen["name"] if isinstance(screen, dict) and "name" in screen else str(screen)
        print(f"🖼️  Generating files for screen: {screen_name}")
        prompt = f"""
You are a senior iOS engineer and software architect.

Your task is to generate the Xcode project structure and Swift files for a new iOS app screen named "{screen_name}", following **UIKit** and **MVVM Clean Architecture** best practices.

**Project Structure:**
- App/
- Core/
- Models/
- Resources/
- Services/
- Utils/
- Views/
- ViewModels/

**Requirements:**
- Use UIKit (not SwiftUI).
- Each screen must have:
    - A `ViewController` in `Views/` (e.g., `{screen_name}ViewController.swift`) using UIKit, with UI built programmatically (no Storyboard/XIB).
    - A `ViewModel` in `ViewModels/` (e.g., `{screen_name}ViewModel.swift`) conforming to `ObservableObject` or using Combine for bindings.
    - A `Model` in `Models/` if needed.
    - Use dependency injection for services.
    - Use Swift 5.9 syntax.
    - Scaffold file headers and class/struct names.
    - Use best practices for folder and file organization.
    - Add comments for clarity where appropriate.

**Respond ONLY in this format:**

--- file: App/AppDelegate.swift
<swift code if needed>

--- file: Views/{screen_name}ViewController.swift
<swift code>

--- file: ViewModels/{screen_name}ViewModel.swift
<swift code>

--- file: Models/{screen_name}Model.swift
<swift code if needed>

--- file: Services/...
<swift code if needed>

--- file: Resources/...
<swift code if needed>

--- file: Utils/...
<swift code if needed>

(Include only the files relevant for this screen. Do not include placeholder files. Do not output anything except the code blocks above.)
"""
        result = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        swift_files[screen_name] = result.choices[0].message.content

    print("✅ [GENERATE_CODE] Generated Swift files for all screens.")
    return {"generated_files": swift_files}