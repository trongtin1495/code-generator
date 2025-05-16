import json
import os
from typing import List, Dict, Any

def load_figma_json(filepath: str) -> Dict[str, Any]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_pages(json_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return json_data.get("document", {}).get("children", [])

def extract_colors(node: Dict[str, Any]) -> set:
    colors = set()
    for child in node.get("children", []):
        fills = child.get("fills", [])
        for fill in fills:
            if fill.get("type") == "SOLID":
                color = fill.get("color")
                if color:
                    hex_color = rgba_to_hex(color)
                    colors.add(hex_color)
    return colors

def rgba_to_hex(rgba: Dict[str, float]) -> str:
    r = int(rgba.get("r", 0) * 255)
    g = int(rgba.get("g", 0) * 255)
    b = int(rgba.get("b", 0) * 255)
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)

def extract_fonts(node: Dict[str, Any]) -> set:
    fonts = set()
    for child in node.get("children", []):
        if child.get("type") == "TEXT":
            style = child.get("style", {})
            family = style.get("fontFamily")
            size = style.get("fontSize")
            if family and size:
                fonts.add(f"{family} {int(size)}pt")
    return fonts

def analyze_figma_json(json_data: Dict[str, Any]) -> Dict[str, Any]:
    pages = extract_pages(json_data)
    summary = {
        "pages": {}
    }
    seen_screens = set()

    if not pages:
        print("❌ No pages found in Figma file.")
        return summary

    # Since you have only 1 screen page, use the first one
    design_page = pages[0]
    page_name = design_page.get("name", "UnnamedPage").strip()

    if design_page.get("type") != "CANVAS":
        print(f"⚠️ Skipping non-canvas page: {page_name}")
        return summary

    screens = []
    for node in design_page.get("children", []):
        if node.get("type") != "FRAME":
            continue

        screen_name = node.get("name", "Unnamed Frame").strip()
        width = node.get("absoluteBoundingBox", {}).get("width")
        height = node.get("absoluteBoundingBox", {}).get("height")
        size = f"{int(width)}x{int(height)}" if width and height else "Unknown"

        components = [child.get("name", "Unnamed") for child in node.get("children", [])]
        colors = extract_colors(node)
        fonts = extract_fonts(node)

        screen_info = {
            "name": screen_name,
            "size": size,
            "components": components,
            "colors": list(colors),
            "fonts": list(fonts)
        }

        screen_key = f"{page_name}-{screen_name}"
        if screen_key not in seen_screens:
            seen_screens.add(screen_key)
            screens.append(screen_info)

    summary["pages"][page_name] = {"screens": screens}
    return summary

def save_summary(summary: Dict[str, Any], out_path: str):
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

def analyze_and_save(input_path: str, output_path: str):
    json_data = load_figma_json(input_path)
    summary = analyze_figma_json(json_data)
    save_summary(summary, output_path)
    print(f"✅ Summary written to: {output_path}")