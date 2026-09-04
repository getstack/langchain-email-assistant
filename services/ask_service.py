"""Ask AI service with optional RAG context."""

from __future__ import annotations

import time

from langchain_core.output_parsers import StrOutputParser

from llm import active_model_name, get_model
from prompts import LENGTH_GUIDANCE, ask_prompt


def ask_ai(
    *,
    question: str,
    tone: str = "Professional",
    length: str = "Medium",
    context: str = "",
) -> dict:
    started = time.perf_counter()
    chain = ask_prompt | get_model(temperature=0.4) | StrOutputParser()
    answer = chain.invoke(
        {
            "question": question,
            "tone": tone,
            "length_guidance": LENGTH_GUIDANCE.get(length, LENGTH_GUIDANCE["Medium"]),
            "context": context or "No extra knowledge context provided.",
        }
    )
    latency_ms = int((time.perf_counter() - started) * 1000)
    return {
        "feature": "ask_ai",
        "subject": "",
        "body": answer.strip(),
        "text": answer.strip(),
        "raw": answer,
        "model": active_model_name(),
        "latency_ms": latency_ms,
        "input_text": question,
    }
