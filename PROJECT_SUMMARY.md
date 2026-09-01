# Project Summary: AI Communication Assistant

Learning and portfolio AI SaaS for writing emails, replying to emails, and asking AI questions — with auth, history, usage tracking, RAG, and LangGraph workflows.

## What It Does

1. Sign in or create an account (Supabase email/password when configured, or local demo `demo` / `demo123`).
2. Choose a mode: **Write Email**, **Reply to Email**, or **Ask AI**.
3. Set tone and length, enter notes (or paste an email to reply to).
4. Click **Generate** — a LangGraph workflow routes the request, retrieves RAG context for Ask AI when useful, generates a draft, then reviews it.
5. View Subject/Body (emails), copy/download, regenerate, or edit.
6. Recent history and usage counters update in the sidebar.
7. Profile lets you change display name, email, and default tone.

## Project Structure

- `app.py` — Streamlit entry / orchestration
- `components/` — sidebar, header, composer, result
- `services/` — write / reply / ask services + router + JSON parsing
- `prompts.py` / `prompt.py` — prompt templates (compat export)
- `chain.py` / `llm.py` — model factory and legacy LCEL export
- `config/` — env / Streamlit secrets (`SUPABASE_URL`, `SUPABASE_ANON_KEY`)
- `auth/` — Supabase Auth + SQLite demo fallback, profile helpers
- `auth/supabase_client.py`, `auth/supabase_auth.py` — Supabase client and session
- `database/` — SQLite history + usage (user profiles via Supabase when enabled)
- `supabase/schema.sql` — Postgres `profiles` table + RLS policies
- `rag/` — document load → split → embed → in-memory cosine retrieve
- `graph/` — LangGraph understand → retrieve? → generate → review
- `knowledge/` — sample docs for RAG
- `utils/` — validation, rate limit, logging
- `styles.py` — SaaS CSS tokens
- `.github/workflows/ci.yml` — install + syntax/import smoke checks

## Architecture

```text
UI (Streamlit)
  -> Auth (Supabase or SQLite demo)
  -> LangGraph workflow
       -> retrieve (Ask AI / RAG)
       -> generate (Write | Reply | Ask services)
       -> review
  -> History + usage (SQLite; Supabase profiles)
```

## Tech Stack

- Python, Streamlit
- LangChain, LangGraph, langchain-google-genai
- Google embeddings + in-memory cosine retrieval (RAG)
- SQLite (history, usage, local demo users)
- Supabase Auth + Postgres profiles (optional)
- python-dotenv

## Current Scope and Roadmap

### Completed

- Phase 0: LCEL Write Email foundation (`v0.1.0`)
- Phase 1: SaaS UI shell
- Phase 2: Structured subject/body + length + email service
- Phase 3: Reply to Email
- Phase 4: Ask AI + routing
- Phase 5: Auth + profile
- Phase 6: History + usage tracking
- Phase 7: Stable product packaging
- Phase 8: RAG knowledge base
- Phase 9: LangGraph workflow
- Phase 10: Validation, rate limiting, logging, CI
- UI polish pass (login card, mode cards, sidebar icons, Generate CTA)
- Header/sidebar layout fix (greeting not clipped; wider sidebar)
- Unified SaaS sign-in / sign-up auth card (purple theme, create account)
- Streamlit theme primaryColor set to purple (fixes red Sign in button)
- Compact RECENT history rows in sidebar (mockup-sized)
- Supabase Auth Phase 1 (email sign-up/sign-in, profiles table, SQLite fallback)

### Planned / next hardening

- Migrate history/usage to Supabase Postgres
- OAuth providers via Supabase
- LangSmith tracing
- Docker / full API split
- Native clipboard copy (beyond download button)

## Run Locally

1. Create and activate `.venv`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set `GOOGLE_API_KEY`
4. Optional Supabase: set `SUPABASE_URL` and `SUPABASE_ANON_KEY`, run `supabase/schema.sql` in Supabase SQL Editor
5. Optional Cloud DB path: `ACA_DB_PATH=/tmp/aca.db`
6. `streamlit run app.py`
7. Sign in with demo / demo123 (local) or your Supabase email account
