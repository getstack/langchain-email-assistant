"""Top header and greeting."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from auth import current_user


def _greeting() -> str:
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    if hour < 18:
        return "Good afternoon"
    return "Good evening"


def render_header() -> None:
    user = current_user()
    left, right = st.columns([3, 1])
    with left:
        name = user["display_name"].split()[0] if user else "there"
        st.markdown(
            f"<h2 class='aca-greeting'>{_greeting()}, {name} 👋</h2>",
            unsafe_allow_html=True,
        )
        st.caption("What would you like to work on today?")
    with right:
        label = user["display_name"] if user else "Guest"
        st.markdown(
            f"<div style='text-align:right;padding-top:0.85rem;color:#4b5563;'>🔔 &nbsp; <strong>{label}</strong> ▾</div>",
            unsafe_allow_html=True,
        )
