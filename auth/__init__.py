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

    left, center, right = st.columns([1, 1.2, 1])
    with center:
        st.markdown(
            """
            <div class="aca-login-wrap">
                <div class="aca-brand">✦ AI Communication Assistant</div>
                <h2>Welcome back</h2>
                <p class="aca-muted">Sign in to write emails, reply, and ask AI.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("Demo account: username `demo` / password `demo123`")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="demo")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Sign in", type="primary", width="stretch")
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
