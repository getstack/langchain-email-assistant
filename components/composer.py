"""Mode cards, composer controls, and generate action."""

from __future__ import annotations

import streamlit as st

from prompts import LENGTHS, TONES


MODE_META = {
    "write": {
        "title": "Write Email",
        "icon": "✉",
        "desc": "Create a new email from scratch",
        "placeholder": "Describe the email you want to write...",
        "input_label": "What do you want to say?",
    },
    "reply": {
        "title": "Reply to Email",
        "icon": "↩",
        "desc": "Generate a response to an email",
        "placeholder": "Optional notes for your reply (points to include)...",
        "input_label": "Guidance for your reply (optional)",
    },
    "ask": {
        "title": "Ask AI",
        "icon": "💬",
        "desc": "Ask questions and get help from AI",
        "placeholder": "Ask a question, e.g. What is REST API?",
        "input_label": "Your question",
    },
}


def render_mode_cards() -> None:
    cols = st.columns(3)
    for col, (key, meta) in zip(cols, MODE_META.items()):
        active = st.session_state.mode == key
        with col:
            st.markdown(
                f"""
                <div class="aca-mode-card {'active' if active else ''}">
                    <div class="aca-icon">{meta['icon']}</div>
                    <h4>{meta['title']}</h4>
                    <p>{meta['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                meta["title"] if not active else f"✓ {meta['title']}",
                key=f"card_{key}",
                type="primary" if active else "secondary",
                width="stretch",
            ):
                st.session_state.mode = key
                st.session_state.result = None
                st.session_state.result_error = None
                st.rerun()


def render_composer() -> tuple[str, str, str, str, bool]:
    mode = st.session_state.mode
    meta = MODE_META[mode]

    original_email = ""
    if mode == "reply":
        original_email = st.text_area(
            "Paste the email you received",
            value=st.session_state.get("original_email", ""),
            placeholder="Paste the original email here...",
            key="original_email_input",
            height=160,
        )
        st.session_state.original_email = original_email

    notes = st.text_area(
        meta["input_label"],
        value=st.session_state.get("notes", ""),
        placeholder=meta["placeholder"],
        key="notes_input",
        height=170,
        max_chars=4000,
    )
    st.session_state.notes = notes
    st.caption(f"{len(notes)} / 4000")

    c1, c2, c3 = st.columns([1.2, 1.2, 1])
    with c1:
        default_tone = st.session_state.get("tone", "Professional")
        tone_index = TONES.index(default_tone) if default_tone in TONES else 0
        tone = st.selectbox("Tone", TONES, index=tone_index)
        st.session_state.tone = tone
    with c2:
        default_length = st.session_state.get("length", "Medium")
        length_index = LENGTHS.index(default_length) if default_length in LENGTHS else 1
        length = st.selectbox("Length", LENGTHS, index=length_index)
        st.session_state.length = length
    with c3:
        st.write("")
        st.write("")
        generate = st.button("✨ Generate", type="primary", width="stretch")

    reply_email = original_email if mode == "reply" else ""
    return notes, tone, length, reply_email, generate
