"""
AI Communication Assistant — Streamlit entry point.

Phases covered:
1) SaaS UI  2) Write Email v2  3) Reply  4) Ask AI
5) Auth/Profile  6) History/Usage  7) Stable product
8) RAG  9) LangGraph  10) Production hardening
"""

from __future__ import annotations

import streamlit as st

from auth import current_user, require_login, save_profile
from components.composer import render_composer, render_mode_cards
from components.header import render_header
from components.result import render_result
from components.sidebar import render_sidebar
from database import add_history, add_usage, get_history_item
from graph import run_workflow
from styles import APP_CSS
from utils import configure_logging, logger, rate_limiter, validate_text

st.set_page_config(
    page_title="AI Communication Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

configure_logging()
st.html(APP_CSS)


def init_state() -> None:
    defaults = {
        "mode": "write",
        "notes": "",
        "original_email": "",
        "tone": "Professional",
        "length": "Medium",
        "result": None,
        "result_error": None,
        "show_profile": False,
        "selected_history_id": None,
        "use_langgraph": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def run_generation() -> None:
    user = current_user()
    mode = st.session_state.mode
    notes = st.session_state.notes
    tone = st.session_state.tone
    length = st.session_state.length
    original_email = st.session_state.original_email

    allowed, limit_msg = rate_limiter.allow(str(user["id"] if user else "anon"))
    if not allowed:
        st.session_state.result_error = limit_msg
        st.session_state.result = None
        return

    if mode == "reply":
        check = validate_text(original_email, field="the original email", min_len=5)
        if not check.ok:
            st.session_state.result_error = check.message
            st.session_state.result = None
            return
    else:
        check = validate_text(notes, field="your input", min_len=3)
        if not check.ok:
            st.session_state.result_error = check.message
            st.session_state.result = None
            return

    feature = {"write": "write_email", "reply": "reply_email", "ask": "ask_ai"}[mode]
    input_for_usage = original_email if mode == "reply" else notes

    try:
        with st.spinner("Generating with AI workflow..."):
            result = run_workflow(
                mode=mode,
                notes=notes,
                tone=tone,
                length=length,
                original_email=original_email,
            )
        st.session_state.result = result
        st.session_state.result_error = None
        logger.info("generation_ok feature=%s latency_ms=%s", feature, result.get("latency_ms"))

        if user:
            title = result.get("subject") or notes[:48] or feature
            add_history(
                user_id=user["id"],
                feature=feature,
                title=title or feature,
                input_text=input_for_usage,
                output_text=result["text"],
                tone=tone,
                length=length,
            )
            add_usage(
                user_id=user["id"],
                feature=feature,
                model=result.get("model", ""),
                input_text=input_for_usage,
                output_text=result["text"],
                latency_ms=int(result.get("latency_ms", 0)),
                status="ok",
            )
    except Exception as exc:
        logger.exception("generation_failed feature=%s", feature)
        st.session_state.result = None
        st.session_state.result_error = f"Generation failed: {exc}"
        if user:
            add_usage(
                user_id=user["id"],
                feature=feature,
                model="",
                input_text=input_for_usage,
                output_text="",
                latency_ms=0,
                status="error",
            )


def render_profile() -> None:
    user = current_user()
    if not user:
        return
    tones = [
        "Professional",
        "Friendly",
        "Formal",
        "Casual",
        "Confident",
        "Polite",
        "Persuasive",
        "Apologetic",
    ]
    st.subheader("Profile")
    with st.form("profile_form"):
        display_name = st.text_input("Display name", value=user["display_name"])
        email = st.text_input("Email", value=user.get("email") or "")
        current_tone = user.get("default_tone") or "Professional"
        tone_index = tones.index(current_tone) if current_tone in tones else 0
        default_tone = st.selectbox("Default tone", tones, index=tone_index)
        saved = st.form_submit_button("Save profile", type="primary")
        if saved:
            save_profile(display_name, email, default_tone)
            st.session_state.tone = default_tone
            st.session_state.show_profile = False
            st.success("Profile saved.")
            st.rerun()
    if st.button("Back to workspace"):
        st.session_state.show_profile = False
        st.rerun()


def load_selected_history() -> None:
    user = current_user()
    item_id = st.session_state.get("selected_history_id")
    if not user or not item_id:
        return
    item = get_history_item(user["id"], item_id)
    st.session_state.selected_history_id = None
    if not item:
        return
    feature_to_mode = {
        "write_email": "write",
        "reply_email": "reply",
        "ask_ai": "ask",
    }
    st.session_state.mode = feature_to_mode.get(item["feature"], "write")
    st.session_state.tone = item.get("tone") or "Professional"
    st.session_state.length = item.get("length") or "Medium"
    if item["feature"] == "reply_email":
        st.session_state.original_email = item.get("input_text") or ""
        st.session_state.notes = ""
    else:
        st.session_state.notes = item.get("input_text") or ""
    st.session_state.result = {
        "feature": item["feature"],
        "subject": "",
        "body": item.get("output_text") or "",
        "text": item.get("output_text") or "",
        "model": "",
        "latency_ms": 0,
    }


def main() -> None:
    init_state()
    if not require_login():
        return

    user = current_user()
    if user and not st.session_state.get("_tone_bootstrapped"):
        st.session_state.tone = user.get("default_tone") or "Professional"
        st.session_state._tone_bootstrapped = True

    load_selected_history()
    render_sidebar()

    if st.session_state.show_profile:
        render_profile()
        return

    render_header()
    render_mode_cards()
    st.divider()

    notes, tone, length, original_email, generate = render_composer()
    st.session_state.notes = notes
    st.session_state.tone = tone
    st.session_state.length = length
    if st.session_state.mode == "reply":
        st.session_state.original_email = original_email

    if generate:
        run_generation()

    def on_regenerate():
        run_generation()

    def on_edit():
        # Put output back into the composer for refinement.
        result = st.session_state.get("result") or {}
        st.session_state.notes = result.get("text") or st.session_state.notes
        st.session_state.result = None
        st.rerun()

    st.divider()
    render_result(on_regenerate=on_regenerate, on_edit=on_edit)


main()
