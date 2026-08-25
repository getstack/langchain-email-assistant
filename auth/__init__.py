"""Simple session-based authentication helpers."""

from __future__ import annotations

import streamlit as st

from database import authenticate, ensure_demo_user, get_user, init_db, update_profile


def bootstrap_auth() -> None:
    init_db()
    ensure_demo_user()
    if "user" not in st.session_state:
        st.session_state.user = None


def require_login() -> bool:
    """Render login form when logged out. Returns True if authenticated."""
    bootstrap_auth()
    if st.session_state.user:
        return True

    st.markdown("### Sign in")
    st.caption("Demo account: username `demo` / password `demo123`")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in", type="primary")
        if submitted:
            user = authenticate(username, password)
            if user:
                st.session_state.user = user
                st.rerun()
            st.error("Invalid username or password.")
    return False


def logout() -> None:
    st.session_state.user = None
    st.rerun()


def current_user() -> dict | None:
    user = st.session_state.get("user")
    if not user:
        return None
    fresh = get_user(user["id"])
    if fresh:
        st.session_state.user = fresh
    return st.session_state.user


def save_profile(display_name: str, email: str, default_tone: str) -> None:
    user = current_user()
    if not user:
        return
    update_profile(user["id"], display_name, email, default_tone)
    st.session_state.user = get_user(user["id"])
