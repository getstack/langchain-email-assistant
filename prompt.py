from langchain_core.prompts import ChatPromptTemplate

email_prompt = ChatPromptTemplate.from_template("""
You are an expert email writing assistant.

Write a {tone} email based on the following notes.

Notes:
{notes}

Only return the email.
""")