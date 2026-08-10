import re


SYSTEM_PROMPT = """
You are a task parsing assistant.

Convert a user's natural-language task description into:
- title
- priority
- due_date_hint

Priority must be exactly:
low, medium, or high.

Use deterministic parsing rules.
Return structured task information.
"""


def build_prompt(description: str):
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": description,
        },
    ]


def mock_parse_task(description: str):
    # Lower-cased copy used only for matching
    lowered = description.lower()

    # ---------------------------------
    # Priority
    # ---------------------------------
    if "urgent" in lowered or "asap" in lowered:
        priority = "high"

    elif (
        "whenever" in lowered
        or "low priority" in lowered
    ):
        priority = "low"

    else:
        priority = "medium"

    # ---------------------------------
    # Due date
    # ---------------------------------
    due_date_hint = None

    date_phrases = [
        "today",
        "tomorrow",
        "next week",
        "next monday",
        "next tuesday",
        "next wednesday",
        "next thursday",
        "next friday",
        "next saturday",
        "next sunday",
    ]

    for phrase in date_phrases:
        if phrase in lowered:
            due_date_hint = phrase
            break

    if due_date_hint is None:
        weekdays = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]

        for day in weekdays:
            if day in lowered:
                due_date_hint = day
                break

    # ---------------------------------
    # Title
    # ---------------------------------
    title = description

    priority_keywords = [
        "urgent",
        "asap",
        "whenever",
        "low priority",
    ]

    for keyword in priority_keywords:
        title = re.sub(
            re.escape(keyword),
            "",
            title,
            flags=re.IGNORECASE,
        )

    if due_date_hint:
        title = re.sub(
            re.escape(due_date_hint),
            "",
            title,
            flags=re.IGNORECASE,
        )

    title = title.strip()

    if not title:
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date_hint": due_date_hint,
    }