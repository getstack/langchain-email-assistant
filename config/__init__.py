"""App configuration from environment variables or Streamlit secrets."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


def _get_secret(key: str) -> str:
    """Read config from env first, then Streamlit secrets (Cloud)."""
    value = os.getenv(key, "").strip()
    if value:
        return value
    try:
        import streamlit as st

        return str(st.secrets.get(key, "")).strip()
    except Exception:
        return ""


def supabase_url() -> str:
    return _get_secret("SUPABASE_URL")


def supabase_anon_key() -> str:
    return _get_secret("SUPABASE_ANON_KEY")


def supabase_enabled() -> bool:
    return bool(supabase_url() and supabase_anon_key())


def llm_provider() -> str:
    """Chat provider: gemini (default) or openrouter."""
    value = _get_secret("LLM_PROVIDER").lower()
    return value if value in {"gemini", "openrouter"} else "gemini"


def openrouter_api_key() -> str:
    return _get_secret("OPENROUTER_API_KEY")


def openrouter_model() -> str:
    return _get_secret("OPENROUTER_MODEL") or "minimax/minimax-m3:free"


def openrouter_max_tokens() -> int:
    raw = _get_secret("OPENROUTER_MAX_TOKENS") or "2048"
    try:
        return max(256, int(raw))
    except ValueError:
        return 2048


def gemini_model_name() -> str:
    return _get_secret("GEMINI_MODEL") or "gemini-2.0-flash"
