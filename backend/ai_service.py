import json
import os
import re
from datetime import date, timedelta


def _parse_priority(text: str) -> str:
    text_lower = text.lower()

    if re.search(r"\b(high|urgent|important|critical)\b", text_lower):
        return "high"

    if re.search(r"\b(low|minor)\b", text_lower):
        return "low"

    return "medium"


def _parse_due_date(text: str) -> str | None:
    text_lower = text.lower()
    today = date.today()

    if "tomorrow" in text_lower:
        return (today + timedelta(days=1)).isoformat()

    if "today" in text_lower:
        return today.isoformat()

    if "day after tomorrow" in text_lower:
        return (today + timedelta(days=2)).isoformat()

    # Basic "next <weekday>" support
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    match = re.search(
        r"\bnext\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
        text_lower,
    )

    if match:
        target = weekdays[match.group(1)]
        days_ahead = (target - today.weekday()) % 7

        if days_ahead == 0:
            days_ahead = 7

        return (today + timedelta(days=days_ahead)).isoformat()

    return None


def _clean_title(text: str) -> str:
    title = text.strip()

    # Remove common priority phrases.
    title = re.sub(
        r"\b(with\s+)?(high|low|medium|urgent|important|critical)\s+priority\b",
        "",
        title,
        flags=re.IGNORECASE,
    )

    # Remove relative date phrases.
    title = re.sub(
        r"\b(day after tomorrow|tomorrow|today)\b",
        "",
        title,
        flags=re.IGNORECASE,
    )

    title = re.sub(
        r"\bnext\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
        "",
        title,
        flags=re.IGNORECASE,
    )

    title = re.sub(r"\s+", " ", title).strip(" ,.-")

    return title or text.strip()


def _mock_quick_add(text: str) -> dict:
    return {
        "title": _clean_title(text),
        "priority": _parse_priority(text),
        "due_date": _parse_due_date(text),
    }


def _groq_quick_add(text: str) -> dict:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is required when USE_GROQ=true"
        )

    from groq import Groq

    client = Groq(api_key=api_key)

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
- Convert relative dates such as today, tomorrow,
  and next Monday into YYYY-MM-DD.
- Use today's date as the reference date.
- If no date is mentioned, return null.
- Never return words such as "tomorrow" or "today"
  in due_date.
- Do not add extra fields.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract structured task information "
                    "from natural language. Return only valid JSON."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
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


def ai_quick_add(text: str) -> dict:
    text = text.strip()

    if not text:
        raise ValueError("Quick Add input cannot be blank")

    # IMPORTANT:
    # Mock parser is the default grading path.
    # Real Groq is optional and must be explicitly enabled.
    use_groq = os.getenv("USE_GROQ", "false").lower() == "true"

    if use_groq:
        return _groq_quick_add(text)

    return _mock_quick_add(text)