import streamlit as st

from chain import email_chain


st.title("🤖 AI Email Assistant")

notes = st.text_area(
    "Describe your email",
    placeholder="Example: Customer sync is completed. Waiting for approval."
)

tone = st.selectbox(
    "Choose tone",
    ["Professional", "Friendly", "Formal", "Casual"]
)

if st.button("Generate Email"):
    if not notes.strip():
        st.warning("Please enter some notes first.")
    else:
        with st.spinner("Generating email..."):
            result = email_chain.invoke({
                "tone": tone,
                "notes": notes
            })

        st.subheader("Generated Email")
        st.write(result)