# AI Communication Assistant

A learning + portfolio AI SaaS built with **Python, Streamlit, LangChain, Google Gemini, RAG, and LangGraph**.

This repository evolved from a simple email generator (`v0.1.0`) into a multi-mode communication assistant with auth, history, usage tracking, retrieval, and workflow orchestration.

---

## Features

- SaaS-style dashboard UI (sidebar, modes, composer, result card)
- **Write Email** with tone + length and structured subject/body
- **Reply to Email**
- **Ask AI** (general Q&A)
- Demo authentication + user profile (Supabase email/password)
- Supabase Postgres history and usage/token estimates
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
SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

Run `supabase/schema.sql` in your Supabase SQL Editor, then start the app:

```powershell
streamlit run app.py
```

Sign up or sign in with your email and password.

---

## Architecture

```text
Streamlit UI
  -> Auth / Profile
  -> LangGraph workflow
       -> RAG retrieve (Ask AI)
       -> Write | Reply | Ask services
       -> Review node
  -> Supabase Auth + Postgres (profiles, history, usage)
```

See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for the phase roadmap and file roles.

---

## Streamlit Cloud

- Main file: `app.py`
- Secrets: `GOOGLE_API_KEY`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`
- Run `supabase/schema.sql` in Supabase before first deploy

---

## Security

Never commit:

- `.env`
- API keys
- passwords / tokens

`.gitignore` already excludes `.env`, `.venv/`, and `__pycache__/`.

---

## License

Educational / learning purposes.
