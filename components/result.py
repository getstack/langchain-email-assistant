"""Result card with copy / regenerate / edit."""

from __future__ import annotations

import html

import streamlit as st


def render_result(*, on_regenerate, on_edit) -> None:
    error = st.session_state.get("result_error")
    result = st.session_state.get("result")

    if error:
        st.error(error)
        return

    if not result:
        st.info("Your generated result will appear here.")
        return

    feature = result.get("feature", "write_email")
    title = {
        "write_email": "Generated Email",
        "reply_email": "Generated Reply",
        "ask_ai": "AI Answer",
    }.get(feature, "Result")

    head, b1, b2, b3 = st.columns([3, 1, 1, 1])
    with head:
        st.subheader(title)
    with b1:
        st.download_button(
            "Copy",
            data=result["text"],
            file_name="generated.txt",
            mime="text/plain",
            width="stretch",
            help="Download the generated text so you can copy it",
        )
    with b2:
        if st.button("Regenerate", width="stretch"):
            on_regenerate()
    with b3:
        if st.button("Edit", width="stretch"):
            on_edit()

    if feature in {"write_email", "reply_email"} and result.get("subject"):
        st.markdown(f"**Subject:** {html.escape(str(result['subject']))}")

    safe_text = html.escape(result["text"]).replace("\n", "<br>")
    st.markdown(
        f'<div class="aca-result-card">{safe_text}</div>',
        unsafe_allow_html=True,
    )
    if result.get("latency_ms"):
        st.caption(f"Latency: {result['latency_ms']} ms · Model: {result.get('model', '')}")
