"""Sidebar navigation and placeholders."""

from __future__ import annotations

import html
import re
import time

import streamlit as st

from auth import current_user, logout
from database import list_history, usage_summary


MODE_LABELS = {
    "write": "✉  Write Email",
    "reply": "↩  Reply to Email",
    "ask": "💬  Ask AI",
}


def _relative_time(ts: float) -> str:
    delta = int(time.time() - ts)
    if delta < 60:
        return "just now"
    if delta < 3600:
        return f"{delta // 60}m ago"
    if delta < 86400:
        return f"{delta // 3600}h ago"
    return f"{delta // 86400}d ago"


def _short_title(title: str, limit: int = 28) -> str:
    """Keep RECENT labels short like the mockup."""
    text = (title or "Untitled").strip()
    text = re.sub(r"\s*[-–—]\s*\[.*?\]", "", text)
    for sep in (" – ", " — ", " - "):
        if sep in text:
            text = text.split(sep)[0].strip()
            break
    if len(text) > limit:
        return text[: limit - 1].rstrip() + "…"
    return text or "Untitled"


def render_sidebar() -> None:
    user = current_user()
    with st.sidebar:
        st.markdown("### ✦ AI Communication Assistant")
        if st.button("+ New", type="primary", width="stretch"):
            st.session_state.mode = "write"
            st.session_state.notes = ""
            st.session_state.original_email = ""
            st.session_state.result = None
            st.session_state.result_error = None
            st.rerun()

        st.caption("MODES")
        for key, label in MODE_LABELS.items():
            selected = st.session_state.get("mode") == key
            if st.button(
                label,
                key=f"nav_{key}",
                type="primary" if selected else "secondary",
                width="stretch",
            ):
                st.session_state.mode = key
                st.session_state.result = None
                st.session_state.result_error = None
                st.rerun()

        st.divider()
        st.caption("RECENT")
        if user:
            items = list_history(user["id"])
            if not items:
                st.markdown(
                    '<p class="aca-muted">No history yet. Generate something!</p>',
                    unsafe_allow_html=True,
                )
            else:
                for item in items:
                    title = _short_title(item["title"])
                    when = _relative_time(item["created_at"])
                    row = st.columns([0.86, 0.14], gap="small")
                    with row[0]:
                        st.markdown(
                            f"""
                            <div class="aca-recent-row">
                                <div class="aca-recent-icon">📄</div>
                                <div class="aca-recent-text">
                                    <div class="aca-recent-title">{html.escape(title)}</div>
                                    <div class="aca-recent-time">{html.escape(when)}</div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    with row[1]:
                        if st.button(
                            "›",
                            key=f"hist_{item['id']}",
                            type="tertiary",
                            help=f"Open: {title}",
                        ):
                            st.session_state.selected_history_id = item["id"]
                            st.rerun()
        else:
            st.markdown(
                '<p class="aca-muted">Sign in to see history.</p>',
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="aca-pro-card">
                <strong>✦ Upgrade to Pro</strong>
                <p class="aca-muted">Unlock higher limits and team features (placeholder).</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if user:
            usage = usage_summary(user["id"])
            st.caption(f"Usage · {usage['requests']} requests · ~{usage['tokens']} tokens")
            initials = "".join(part[0] for part in user["display_name"].split()[:2]).upper() or "U"
            st.markdown(f"**{initials}** · {user['display_name']}")
            st.caption(user.get("email") or user["username"])
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Profile", width="stretch"):
                    st.session_state.show_profile = True
                    st.rerun()
            with c2:
                if st.button("Logout", width="stretch"):
                    logout()
