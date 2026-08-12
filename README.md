# 🤖 AI Email Assistant

A simple AI-powered email assistant built with **Python, LangChain, Google Gemini, and Streamlit**.

This project was created as a hands-on learning project to understand the fundamentals of **LangChain**, including prompt templates, LLM integration, output parsers, and LCEL chains.

The goal is to keep the application simple while building a solid foundation for more advanced AI applications such as **RAG, agents, and LangGraph workflows**.

---

## ✨ Features

* 📝 Generate emails from simple notes
* 🎯 Choose the email tone

  * Professional
  * Friendly
  * Formal
  * Casual
* 🤖 Google Gemini integration
* 🔗 LangChain pipeline using LCEL
* 🧩 Reusable prompt templates
* 📤 Clean text output using `StrOutputParser`
* 🖥️ Simple Streamlit web interface
* 🔐 Environment-based API key configuration

---

## 🏗️ Architecture

The application follows a simple LangChain pipeline:

```text
                     User
                       │
                       ▼
              ┌─────────────────┐
              │   Streamlit UI  │
              │     app.py      │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Prompt Template │
              │    prompt.py    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Gemini Model   │
              │    chain.py     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Output Parser   │
              │ StrOutputParser │
              └────────┬────────┘
                       │
                       ▼
                Generated Email
```

The LangChain pipeline is:

```python
email_chain = email_prompt | model | parser
```

This demonstrates **LCEL (LangChain Expression Language)**, where the output of each component is passed to the next component.

---

## 🧠 LangChain Concepts Demonstrated

### 1. ChatPromptTemplate

A reusable prompt template is defined in `prompt.py`.

```python
email_prompt = ChatPromptTemplate.from_template("""
You are an expert email writing assistant.

Write a {tone} email based on the following notes.

Notes:
{notes}

Only return the email.
""")
```

The `{tone}` and `{notes}` values are dynamically provided by the user.

---

### 2. Chat Model

Google Gemini is connected through LangChain:

```python
model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.7,
)
```

---

### 3. Output Parser

The model returns an AI message object. `StrOutputParser` converts the response into a clean string:

```python
parser = StrOutputParser()
```

---

### 4. LCEL

The components are connected using the LangChain pipe operator:

```python
email_chain = email_prompt | model | parser
```

The flow is:

```text
Prompt → Gemini → Parser → String
```

---

### 5. Invoke

The chain is executed using:

```python
email_chain.invoke({
    "tone": tone,
    "notes": notes
})
```

This sends the user's data through the complete LangChain pipeline.

---

# 📁 Project Structure

```text
email-assistant/
│
├── app.py              # Streamlit user interface
├── chain.py            # LangChain model and chain
├── prompt.py           # Prompt templates
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── .gitignore          # Files excluded from Git
│
├── .env                # API key (local only)
└── .venv/              # Python virtual environment (local only)
```

> `.env` and `.venv` are intentionally excluded from GitHub.

---

# 🚀 Getting Started

Follow these steps to run the project locally.

## 1. Clone the repository

```bash
git clone https://github.com/getstack/langchain-email-assistant.git
```

Move into the project directory:

```bash
cd langchain-email-assistant
```

---

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see:

```text
(.venv)
```

in your terminal.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create a Gemini API key

Create a Gemini API key through **Google AI Studio**.

Then create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 🔐 Security

**Never commit your `.env` file to GitHub.**

The `.gitignore` already contains:

```gitignore
.env
.venv/
__pycache__/
```

If you accidentally expose an API key, revoke it immediately and create a new one.

---

# ▶️ Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

You should see:

```text
🤖 AI Email Assistant

Describe your email

[ Your notes here... ]

Choose tone

[ Professional ▼ ]

[ Generate Email ]
```

Enter your notes, select a tone, and click **Generate Email**.

---

# 💡 Example

### Input

```text
Customer sync is completed.
Sales order sync is still in progress.
Need to update the client.
```

### Tone

```text
Professional
```

### Generated Output

```text
Hi John,

I wanted to provide you with a quick update.

The customer sync has been completed successfully.
The Sales Order sync is currently still in progress.

I will keep you updated once the remaining work is completed.

Best regards,
Ali
```

---

# 🛠️ Tech Stack

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Application development         |
| LangChain     | LLM application framework       |
| Google Gemini | Generative AI model             |
| Streamlit     | Web UI                          |
| python-dotenv | Environment variable management |

---

# 🎯 Learning Roadmap

This project is intentionally being developed incrementally.

### Phase 1 — LangChain Fundamentals

* [x] Prompt templates
* [x] Gemini integration
* [x] Output parsers
* [x] LCEL chains
* [x] Chain invocation
* [x] Streamlit integration

### Phase 2 — Improving the Assistant

* [ ] Better email formatting
* [ ] Email subject generation
* [ ] Reply-to-email functionality
* [ ] Email length control
* [ ] Streaming responses
* [ ] Conversation history

### Phase 3 — RAG

* [ ] Document ingestion
* [ ] Text splitting
* [ ] Embeddings
* [ ] Vector database
* [ ] Retrieval
* [ ] Context-aware email generation

### Phase 4 — LangGraph

* [ ] Graph-based workflows
* [ ] Multiple nodes
* [ ] Conditional routing
* [ ] Agent workflows
* [ ] Human-in-the-loop approval

---

# 🧪 Why This Project?

The purpose of this project is not to build a complex production application immediately.

It is designed as a practical learning path for understanding how modern LLM applications are constructed.

The application starts with:

```text
User Input
    ↓
Prompt
    ↓
LLM
    ↓
Output
```

and will gradually evolve into more advanced architectures involving:

```text
RAG
 ↓
Retrieval
 ↓
Context
 ↓
LLM
```

and eventually:

```text
LangGraph
 ↓
Multiple Nodes
 ↓
Conditional Logic
 ↓
AI Workflows
```

---

# 🤝 Contributing

This project is primarily a learning project, but suggestions and improvements are welcome.

If you find a bug or have an idea for improving the application, feel free to open an issue or submit a pull request.

---

# 📄 License

This project is available for educational and learning purposes.

---

## ⭐ If You Find This Project Useful

If you're learning **LangChain, RAG, or LangGraph**, feel free to explore the code, experiment with it, and build your own version.

More AI projects will be added as the learning journey continues.
