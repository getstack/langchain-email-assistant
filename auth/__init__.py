"""Supabase authentication and session helpers."""

from __future__ import annotations

import streamlit as st

from . import supabase_auth
from config import supabase_enabled


def bootstrap_auth() -> None:
    if "user" not in st.session_state:
        st.session_state.user = None
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "signin"
    if supabase_enabled():
        supabase_auth.restore_session()


def _show_config_error() -> None:
    st.error("Supabase is not configured.")
    st.markdown(
        """
        Add these to your `.env` file (or Streamlit secrets):

        ```
        SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
        SUPABASE_ANON_KEY=your_anon_key_here
        ```

        Then run `supabase/schema.sql` in the Supabase SQL Editor.
        """
    )


def require_login() -> bool:
    """Render sign-in / sign-up when logged out. Returns True if authenticated."""
    bootstrap_auth()
    if not supabase_enabled():
        _show_config_error()
        return False
    if st.session_state.user:
        return True

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
                    else:
                        user, err = supabase_auth.sign_up(email, password, display_name)
                        if err:
                            st.error(err)
                        elif user:
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
                email = st.text_input("Email", placeholder="you@example.com", key="si_email")
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="••••••••",
                    key="si_pass",
                )
                if st.button("Sign in", type="primary", width="stretch", key="si_btn"):
                    user, err = supabase_auth.sign_in(email, password)
                    if err:
                        st.error(err)
                    elif user:
                        st.rerun()

    return False


def logout() -> None:
    supabase_auth.sign_out()
    st.rerun()


def current_user() -> dict | None:
    return st.session_state.get("user")


def save_profile(display_name: str, email: str, default_tone: str) -> None:
    supabase_auth.save_profile(display_name, email, default_tone)
