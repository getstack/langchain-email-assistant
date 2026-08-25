"""Reply to Email service."""

from __future__ import annotations

import time

from langchain_core.output_parsers import StrOutputParser

from llm import MODEL_NAME, get_model
from prompts import LENGTH_GUIDANCE, reply_prompt
from services import format_email_result, parse_email_json


def generate_reply(
    *,
    original_email: str,
    notes: str = "",
    tone: str = "Professional",
    length: str = "Medium",
) -> dict:
    started = time.perf_counter()
    chain = reply_prompt | get_model() | StrOutputParser()
    raw = chain.invoke(
        {
            "original_email": original_email,
            "notes": notes or "Write a helpful reply.",
            "tone": tone,
            "length_guidance": LENGTH_GUIDANCE.get(length, LENGTH_GUIDANCE["Medium"]),
        }
    )
    parsed = parse_email_json(raw)
    latency_ms = int((time.perf_counter() - started) * 1000)
    return {
        "feature": "reply_email",
        "subject": parsed["subject"],
        "body": parsed["body"],
        "text": format_email_result(parsed),
        "raw": raw,
        "model": MODEL_NAME,
        "latency_ms": latency_ms,
        "input_text": original_email,
    }
