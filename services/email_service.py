"""Write Email service — structured subject/body generation."""

from __future__ import annotations

import time

from langchain_core.output_parsers import StrOutputParser

from llm import active_model_name, get_model
from prompts import LENGTH_GUIDANCE, email_prompt
from services import format_email_result, parse_email_json


def generate_email(*, notes: str, tone: str, length: str = "Medium") -> dict:
    started = time.perf_counter()
    chain = email_prompt | get_model() | StrOutputParser()
    raw = chain.invoke(
        {
            "notes": notes,
            "tone": tone,
            "length_guidance": LENGTH_GUIDANCE.get(length, LENGTH_GUIDANCE["Medium"]),
        }
    )
    parsed = parse_email_json(raw)
    latency_ms = int((time.perf_counter() - started) * 1000)
    return {
        "feature": "write_email",
        "subject": parsed["subject"],
        "body": parsed["body"],
        "text": format_email_result(parsed),
        "raw": raw,
        "model": active_model_name(),
        "latency_ms": latency_ms,
        "input_text": notes,
    }
