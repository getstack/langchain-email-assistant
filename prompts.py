"""All chat prompt templates for Write Email, Reply, and Ask AI."""

from langchain_core.prompts import ChatPromptTemplate

TONES = [
    "Professional",
    "Friendly",
    "Formal",
    "Casual",
    "Confident",
    "Polite",
    "Persuasive",
    "Apologetic",
]

LENGTHS = ["Short", "Medium", "Long"]

LENGTH_GUIDANCE = {
    "Short": "Keep it brief (about 3-5 sentences).",
    "Medium": "Use a clear medium length (1-2 short paragraphs).",
    "Long": "Write a fuller email with more detail and context.",
}

email_prompt = ChatPromptTemplate.from_template(
    """
You are an expert email writing assistant for a SaaS product called AI Communication Assistant.

Write a {tone} email based on the following notes.
Length guidance: {length_guidance}

Notes:
{notes}

Return ONLY valid JSON with this exact shape (no markdown fences):
{{"subject": "...", "body": "..."}}
"""
)

reply_prompt = ChatPromptTemplate.from_template(
    """
You are an expert email reply assistant.

Write a {tone} reply to the email below.
Length guidance: {length_guidance}

Optional guidance from the user:
{notes}

Original email:
{original_email}

Return ONLY valid JSON with this exact shape (no markdown fences):
{{"subject": "...", "body": "..."}}
"""
)

ask_prompt = ChatPromptTemplate.from_template(
    """
You are a helpful AI assistant inside AI Communication Assistant.

Answer the user's question clearly and accurately.
Tone preference: {tone}
Length guidance: {length_guidance}

Knowledge context rules:
- If knowledge context below is NOT empty, answer using that context as the primary source.
- Prefer quoting or paraphrasing the provided guidelines/facts.
- Do NOT say you lack company guidelines when the context contains them.
- If the context is empty, say that no knowledge context was retrieved and answer briefly from general knowledge.

Knowledge context:
{context}

Question:
{question}

Return a clear plain-text answer (not JSON).
"""
)

review_prompt = ChatPromptTemplate.from_template(
    """
You review AI-generated communication drafts.

Check the draft for clarity, tone match ({tone}), and completeness.
If it is already good, return it unchanged.
If it needs improvement, return an improved version.

Draft:
{draft}

Return ONLY the final draft text (email JSON string or answer text as provided).
"""
)
