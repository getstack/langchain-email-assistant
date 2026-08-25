# AI Communication Assistant

A learning + portfolio AI SaaS built with **Python, Streamlit, LangChain, Google Gemini, RAG, and LangGraph**.

This repository evolved from a simple email generator (`v0.1.0`) into a multi-mode communication assistant with auth, history, usage tracking, retrieval, and workflow orchestration.

---

## Features

- SaaS-style dashboard UI (sidebar, modes, composer, result card)
- **Write Email** with tone + length and structured subject/body
- **Reply to Email**
- **Ask AI** (general Q&A)
- Demo authentication + user profile
- SQLite history and usage/token estimates
- RAG over files in `knowledge/`
- LangGraph workflow: understand → retrieve? → generate → review
- Input validation, rate limiting, logging, GitHub Actions CI

---

## Quick start (Windows PowerShell)

```powershell
cd "D:\AI Projects\email-assistant"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.env` (never commit this file):

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Run:

```powershell
streamlit run app.py
```

Demo login:

- Username: `demo`
- Password: `demo123`

---

## Architecture

```text
Streamlit UI
  -> Auth / Profile
  -> LangGraph workflow
       -> RAG retrieve (Ask AI)
       -> Write | Reply | Ask services
       -> Review node
  -> SQLite history + usage
```

See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for the phase roadmap and file roles.

---

## Streamlit Cloud

- Main file: `app.py`
- Secret: `GOOGLE_API_KEY`
- Recommended secret/env for writable DB: `ACA_DB_PATH=/tmp/aca.db`

---

## Security

Never commit:

- `.env`
- API keys
- passwords / tokens

`.gitignore` already excludes `.env`, `.venv/`, `__pycache__/`, and `*.db`.

---

## License

Educational / learning purposes.
