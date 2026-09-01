# Daily Git Workflow (PowerShell)

Use this routine to push progress every day while building Supabase + SaaS features.

## Morning — start work

```powershell
cd "D:\AI Projects\email-assistant"
git checkout main
git pull origin main
git checkout feature/supabase-auth
git merge main
```

If the feature branch does not exist yet:

```powershell
git checkout -b feature/supabase-auth
```

## During the day — save progress

```powershell
git status
git add <files you changed>
git commit -m "Describe what you learned or built today"
git push -u origin feature/supabase-auth
```

## End of day — push even if small

```powershell
git add .
git commit -m "Daily progress: <short summary>"
git push origin feature/supabase-auth
```

## When a feature is ready

```powershell
# Open PR on GitHub: feature/supabase-auth -> main
# After review + local test, merge PR
git checkout main
git pull origin main
```

## Rules

- Never commit `.env` or API keys
- Work on a **feature branch**, not directly on `main`
- One clear commit message per logical change
- Tag milestones: `v0.5.0` for Supabase auth, etc.

## Streamlit Cloud secrets (when deploying)

```toml
GOOGLE_API_KEY = "..."
SUPABASE_URL = "https://YOUR_PROJECT_REF.supabase.co"
SUPABASE_ANON_KEY = "..."
ACA_DB_PATH = "/tmp/aca.db"
```
