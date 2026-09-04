# Daily Git Workflow (PowerShell)

Use this routine to push progress every day. Work on **`staging`** first; merge to **`main`** when ready for production. **Never delete `staging`.**

## Branch model

```text
feature/*  →  staging  →  main (production)
```

- `staging` — long-lived integration branch (keep forever)
- `main` — production (Streamlit Cloud)
- Optional short-lived `feature/*` branches for larger work

## Morning — start work

```powershell
cd "D:\AI Projects\email-assistant"
git checkout staging
git pull origin staging
```

## During the day — save progress

```powershell
git status
git add <files you changed>
git commit -m "Describe what you learned or built today"
git push -u origin staging
```

## End of day — push even if small

```powershell
git add .
git commit -m "Daily progress: <short summary>"
git push origin staging
```

## When staging is ready for production

```powershell
# Prefer a PR: staging -> main (do NOT delete staging after merge)
# Or locally:
git checkout main
git pull origin main
git merge staging
git push origin main

git checkout staging
```

## Rules

- Never commit `.env` or API keys
- Prefer **`staging`** for ongoing work; do not delete it after merging to `main`
- One clear commit message per logical change
- Tag milestones on `main` when needed

## Streamlit Cloud secrets (when deploying)

```toml
GOOGLE_API_KEY = "..."
SUPABASE_URL = "https://YOUR_PROJECT_REF.supabase.co"
SUPABASE_ANON_KEY = "..."
LLM_PROVIDER = "openrouter"
OPENROUTER_API_KEY = "sk-or-v1-..."
OPENROUTER_MODEL = "minimax/minimax-m3:free"
OPENROUTER_MAX_TOKENS = "2048"
```
