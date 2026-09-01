"""Session-based authentication — Supabase when configured, SQLite demo fallback."""

from __future__ import annotations

import streamlit as st

from config import supabase_enabled
from database import (
    authenticate,
    create_user,
    ensure_demo_user,
    get_user,
    init_db,
    update_profile,
)

if supabase_enabled():
    from . import supabase_auth


def bootstrap_auth() -> None:
    init_db()
    if not supabase_enabled():
        ensure_demo_user()
    if "user" not in st.session_state:
        st.session_state.user = None
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "signin"
    if supabase_enabled():
        supabase_auth.restore_session()


def require_login() -> bool:
    """Render sign-in / sign-up when logged out. Returns True if authenticated."""
    bootstrap_auth()
    if st.session_state.user:
        return True

    use_supabase = supabase_enabled()

    left, center, right = st.columns([1, 1.15, 1])
    with center:
        choice = st.segmented_control(
            "Auth mode",
            options=["signin", "signup"],
            format_func=lambda v: "Sign in" if v == "signin" else "Sign up",
            key="auth_mode",
            label_visibility="collapsed",
            width="stretch",
        )
        mode = choice or st.session_state.get("auth_mode") or "signin"
        is_signup = mode == "signup"

        with st.container(border=True):
            if is_signup:
                st.markdown(
                    """
                    <div class="aca-auth-brand">
                        <div class="aca-brand">✦ AI Communication Assistant</div>
                        <h2>Create your account</h2>
                        <p class="aca-muted">Join to write emails, reply, and ask AI.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                display_name = st.text_input(
                    "Display name", placeholder="Muhamad Waqas", key="su_name"
                )
                email = st.text_input("Email", placeholder="you@example.com", key="su_email")
                if not use_supabase:
                    username = st.text_input("Username", placeholder="muhamad", key="su_user")
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="At least 6 characters",
                    key="su_pass",
                )
                password2 = st.text_input(
                    "Confirm password",
                    type="password",
                    placeholder="Repeat password",
                    key="su_pass2",
                )
                if st.button("Create account", type="primary", width="stretch", key="su_btn"):
                    if password != password2:
                        st.error("Passwords do not match.")
                    elif use_supabase:
                        user, err = supabase_auth.sign_up(email, password, display_name)
                        if err:
                            st.error(err)
                        elif user:
                            st.rerun()
                    else:
                        user, err = create_user(
                            username=username,
                            password=password,
                            display_name=display_name,
                            email=email,
                        )
                        if err:
                            st.error(err)
                        else:
                            st.session_state.user = user
                            st.rerun()
            else:
                st.markdown(
                    """
                    <div class="aca-auth-brand">
                        <div class="aca-brand">✦ AI Communication Assistant</div>
                        <h2>Welcome back</h2>
                        <p class="aca-muted">Sign in to write emails, reply, and ask AI.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if not use_supabase:
                    st.markdown(
                        '<p class="aca-demo-hint">Demo account: <code>demo</code> / <code>demo123</code></p>',
                        unsafe_allow_html=True,
                    )
                    username = st.text_input("Username", placeholder="demo", key="si_user")
                else:
                    email = st.text_input("Email", placeholder="you@example.com", key="si_email")
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="••••••••",
                    key="si_pass",
                )
                if st.button("Sign in", type="primary", width="stretch", key="si_btn"):
                    if use_supabase:
                        user, err = supabase_auth.sign_in(email, password)
                        if err:
                            st.error(err)
                        elif user:
                            st.rerun()
                    else:
                        user = authenticate(username, password)
                        if user:
                            st.session_state.user = user
                            st.rerun()
                        st.error("Invalid username or password.")

    return False


def logout() -> None:
    if supabase_enabled() and st.session_state.get("user", {}).get("auth_provider") == "supabase":
        supabase_auth.sign_out()
    else:
        st.session_state.user = None
    st.rerun()


def current_user() -> dict | None:
    user = st.session_state.get("user")
    if not user:
        return None
    if user.get("auth_provider") == "supabase":
        return user
    fresh = get_user(user["id"])
    if fresh:
        st.session_state.user = fresh
    return st.session_state.user


def save_profile(display_name: str, email: str, default_tone: str) -> None:
    user = current_user()
    if not user:
        return
    if user.get("auth_provider") == "supabase":
        supabase_auth.save_profile(display_name, email, default_tone)
        return
    update_profile(user["id"], display_name, email, default_tone)
    st.session_state.user = get_user(user["id"])
