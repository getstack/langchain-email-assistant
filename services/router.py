"""Mode router — selects Write / Reply / Ask services."""

from __future__ import annotations

from services.ask_service import ask_ai
from services.email_service import generate_email
from services.reply_service import generate_reply


def route_generate(
    *,
    mode: str,
    notes: str,
    tone: str,
    length: str,
    original_email: str = "",
    context: str = "",
) -> dict:
    if mode == "reply":
        return generate_reply(
            original_email=original_email,
            notes=notes,
            tone=tone,
            length=length,
        )
    if mode == "ask":
        return ask_ai(
            question=notes,
            tone=tone,
            length=length,
            context=context,
        )
    return generate_email(notes=notes, tone=tone, length=length)
