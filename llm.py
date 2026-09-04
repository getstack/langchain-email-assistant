"""Shared chat model factory (Gemini or OpenRouter MiniMax)."""

from __future__ import annotations

from typing import Any

from config import (
    gemini_model_name,
    llm_provider,
    openrouter_api_key,
    openrouter_max_tokens,
    openrouter_model,
)


def active_model_name() -> str:
    """Model id recorded in usage/history for the active provider."""
    if llm_provider() == "openrouter":
        return openrouter_model()
    return gemini_model_name()


# Back-compat for services that import MODEL_NAME at module load.
MODEL_NAME = active_model_name()


def get_model(temperature: float = 0.7) -> Any:
    provider = llm_provider()

    if provider == "openrouter":
        from langchain_openai import ChatOpenAI

        api_key = openrouter_api_key()
        if not api_key:
            raise RuntimeError(
                "LLM_PROVIDER=openrouter but OPENROUTER_API_KEY is missing. "
                "Set it in .env or Streamlit secrets."
            )
        return ChatOpenAI(
            model=openrouter_model(),
            temperature=temperature,
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            max_tokens=openrouter_max_tokens(),
            default_headers={
                "HTTP-Referer": "https://langchain-email-assistant-fn8avajbmpz6ynepebbsdm.streamlit.app",
                "X-Title": "AI Communication Assistant",
            },
        )

    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(
        model=gemini_model_name(),
        temperature=temperature,
    )
