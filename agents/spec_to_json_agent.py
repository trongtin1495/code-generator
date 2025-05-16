import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic()

def markdown_to_json(markdown: str) -> str:
    prompt = f"""
You are an expert iOS engineer. Convert the following **Markdown specification** into a **pure JSON schema**.

⚠️ Very important: **Only return raw, valid JSON. No explanation, no comments.**

Example output:
{{
  "screens": ["Login", "Home"],
  "components": {{
    "Login": ["TextField", "LoginButton"],
    "Home": ["Header", "FeedList"]
  }},
  "services": ["AuthService", "DataFetcher"],
  "ci": true,
  "docs": true
}}

Markdown:
{markdown}
"""

    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=2048,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()