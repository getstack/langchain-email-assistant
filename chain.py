from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from prompt import email_prompt


# Load environment variables
load_dotenv()


# Initialize Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.7,
)


# Convert AI response to plain text
parser = StrOutputParser()


# Build the LangChain pipeline
email_chain = email_prompt | model | parser