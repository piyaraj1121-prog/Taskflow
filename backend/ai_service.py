import json
import os
from datetime import date

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


def ai_quick_add(user_input: str) -> dict:
    text = user_input.strip()

    if not text:
        raise ValueError("Quick Add input cannot be blank")

    if client is None:
        return {
            "title": text,
            "priority": "medium",
            "due_date": None,
        }

    today = date.today().isoformat()

    prompt = f"""
Convert the following task request into JSON.

Task request:
{text}

Today's date is {today}.

Return ONLY valid JSON with exactly these fields:
{{
  "title": "string",
  "priority": "low | medium | high",
  "due_date": "YYYY-MM-DD or null"
}}

Rules:
- Keep the title concise.
- If priority is not mentioned, use "medium".
- Convert relative dates such as "today", "tomorrow", and "next Monday" into an exact YYYY-MM-DD date.
- Use today's date as the reference date.
- If no date is mentioned, return null.
- Never return words like "tomorrow" or "today" in due_date.
- Do not add extra fields.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You extract structured task information from natural language. Return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content.strip()

    try:
        result = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError("Groq returned invalid JSON") from exc

    priority = result.get("priority", "medium")

    if priority not in {"low", "medium", "high"}:
        priority = "medium"

    return {
        "title": str(result.get("title", text)).strip(),
        "priority": priority,
        "due_date": result.get("due_date"),
    }
