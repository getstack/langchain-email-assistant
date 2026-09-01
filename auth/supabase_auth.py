"""Supabase Auth: sign up, sign in, profile, session restore."""

from __future__ import annotations

from typing import Any

import streamlit as st

from auth.supabase_client import get_supabase_client
from config import supabase_enabled


def _user_from_session(session, profile: dict | None = None) -> dict[str, Any]:
    user = session.user
    meta = user.user_metadata or {}
    prof = profile or {}
    return {
        "id": user.id,
        "email": user.email or "",
        "username": (user.email or "").split("@")[0],
        "display_name": prof.get("display_name") or meta.get("display_name") or "User",
        "default_tone": prof.get("default_tone") or meta.get("default_tone") or "Professional",
        "auth_provider": "supabase",
    }


def _store_session(session) -> dict[str, Any]:
    st.session_state.sb_access_token = session.access_token
    st.session_state.sb_refresh_token = session.refresh_token
    profile = fetch_profile(session.user.id)
    user = _user_from_session(session, profile)
    st.session_state.user = user
    return user


def restore_session() -> dict[str, Any] | None:
    """Re-attach Supabase session after Streamlit reruns."""
    if not supabase_enabled():
        return None
    if st.session_state.get("user") and st.session_state.user.get("auth_provider") == "supabase":
        return st.session_state.user
    access = st.session_state.get("sb_access_token")
    refresh = st.session_state.get("sb_refresh_token")
    if not access or not refresh:
        return None
    try:
        client = get_supabase_client()
        session = client.auth.set_session(access, refresh)
        if session and session.user:
            return _store_session(session)
    except Exception:
        st.session_state.sb_access_token = None
        st.session_state.sb_refresh_token = None
        st.session_state.user = None
    return None


def fetch_profile(user_id: str) -> dict | None:
    try:
        client = get_supabase_client()
        res = client.table("profiles").select("*").eq("id", user_id).limit(1).execute()
        rows = res.data or []
        return rows[0] if rows else None
    except Exception:
        return None


def upsert_profile(user_id: str, display_name: str, default_tone: str = "Professional") -> None:
    client = get_supabase_client()
    client.table("profiles").upsert(
        {
            "id": user_id,
            "display_name": display_name,
            "default_tone": default_tone,
        }
    ).execute()


def sign_up(email: str, password: str, display_name: str) -> tuple[dict[str, Any] | None, str]:
    email = email.strip().lower()
    display_name = display_name.strip()
    if not email or "@" not in email:
        return None, "Please enter a valid email address."
    if len(password) < 6:
        return None, "Password must be at least 6 characters."
    if not display_name:
        return None, "Please enter your display name."

    try:
        client = get_supabase_client()
        res = client.auth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {"data": {"display_name": display_name}},
            }
        )
        if not res.user:
            return None, "Sign up failed. Please try again."

        # Email confirmation may be required depending on Supabase settings.
        if res.session:
            upsert_profile(res.user.id, display_name)
            return _store_session(res.session), ""

        return None, "Account created. Check your email to confirm, then sign in."
    except Exception as exc:
        return None, f"Sign up failed: {exc}"


def sign_in(email: str, password: str) -> tuple[dict[str, Any] | None, str]:
    email = email.strip().lower()
    try:
        client = get_supabase_client()
        res = client.auth.sign_in_with_password({"email": email, "password": password})
        if not res.session or not res.user:
            return None, "Invalid email or password."
        profile = fetch_profile(res.user.id)
        if not profile:
            meta = res.user.user_metadata or {}
            upsert_profile(
                res.user.id,
                meta.get("display_name") or email.split("@")[0],
            )
        return _store_session(res.session), ""
    except Exception as exc:
        return None, f"Sign in failed: {exc}"


def sign_out() -> None:
    try:
        if supabase_enabled() and st.session_state.get("sb_access_token"):
            get_supabase_client().auth.sign_out()
    except Exception:
        pass
    st.session_state.user = None
    st.session_state.sb_access_token = None
    st.session_state.sb_refresh_token = None


def save_profile(display_name: str, email: str, default_tone: str) -> None:
    user = st.session_state.get("user")
    if not user or user.get("auth_provider") != "supabase":
        return
    upsert_profile(user["id"], display_name.strip(), default_tone)
    user["display_name"] = display_name.strip()
    user["email"] = email.strip()
    user["default_tone"] = default_tone
    st.session_state.user = user
