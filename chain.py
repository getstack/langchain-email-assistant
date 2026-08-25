"""Backward-compatible LangChain exports used by older imports. """

from langchain_core.output_parsers import StrOutputParser

from llm import get_model
from prompts import email_prompt

model = get_model()
parser = StrOutputParser()
email_chain = email_prompt | model | parser
