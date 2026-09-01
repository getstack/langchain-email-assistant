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
