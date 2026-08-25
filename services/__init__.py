"""JSON parsing helpers for structured email outputs."""

from __future__ import annotations

import json
import re
from typing import Any


def parse_email_json(raw: str) -> dict[str, str]:
    text = (raw or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        data = json.loads(text)
        if isinstance(data, dict) and "body" in data:
            return {
                "subject": str(data.get("subject", "Update")).strip() or "Update",
                "body": str(data.get("body", "")).strip(),
            }
    except json.JSONDecodeError:
        pass

    # Fallback: treat whole response as body
    subject = "Update"
    body = text
    subject_match = re.search(r"(?im)^subject:\s*(.+)$", text)
    if subject_match:
        subject = subject_match.group(1).strip()
        body = re.sub(r"(?im)^subject:\s*.+$", "", text, count=1).strip()
    return {"subject": subject, "body": body}


def format_email_result(data: dict[str, Any]) -> str:
    return f"Subject: {data.get('subject', 'Update')}\n\n{data.get('body', '')}".strip()
