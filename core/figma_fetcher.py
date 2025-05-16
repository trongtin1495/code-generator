import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()

def download_figma_file(file_key: str, output_path: str):
    access_token = os.getenv("FIGMA_ACCESS_TOKEN")
    if not access_token:
        raise Exception("❌ FIGMA_ACCESS_TOKEN not set in environment!")

    headers = {"X-Figma-Token": access_token}
    url = f"https://api.figma.com/v1/files/{file_key}"

    print(f"🌐 Fetching Figma file: {file_key}")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"❌ Failed to fetch: {response.status_code}\n{response.text}")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(response.json(), f, indent=2)
    print(f"✅ Figma file saved to: {output_path}")