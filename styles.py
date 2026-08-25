"""Shared SaaS theme CSS for AI Communication Assistant."""

APP_CSS = """
<style>
    :root {
        --aca-purple: #6d28d9;
        --aca-purple-soft: #ede9fe;
        --aca-lavender: #a78bfa;
        --aca-bg: #f7f5ff;
        --aca-card: #ffffff;
        --aca-text: #1e1b4b;
        --aca-muted: #6b7280;
        --aca-radius: 14px;
        --aca-shadow: 0 8px 24px rgba(109, 40, 217, 0.08);
        --aca-border: #e8e4f5;
    }

    .stApp, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top right, #efe9ff 0%, var(--aca-bg) 42%, #f8fafc 100%);
        color: var(--aca-text);
    }

    .block-container {
        padding-top: 1.1rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1080px;
    }

    h1, h2, h3 {
        color: var(--aca-text) !important;
        letter-spacing: -0.02em;
    }

    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid var(--aca-border);
    }

    section[data-testid="stSidebar"] .stButton > button {
        border-radius: 12px !important;
        width: 100%;
        justify-content: flex-start;
        font-weight: 500 !important;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: var(--aca-radius) !important;
        border: 1px solid var(--aca-border) !important;
        background: var(--aca-card) !important;
        box-shadow: var(--aca-shadow);
        min-height: 150px;
    }

    div[data-testid="stSelectbox"] > div {
        border-radius: var(--aca-radius) !important;
    }

    div[data-testid="stButton"] > button[kind="primary"] {
        border-radius: var(--aca-radius) !important;
        background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 18px rgba(109, 40, 217, 0.28);
    }

    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background: #5b21b6 !important;
        color: #ffffff !important;
    }

    div[data-testid="stButton"] > button[kind="secondary"] {
        border-radius: 12px !important;
        border: 1px solid var(--aca-border) !important;
        background: #fff !important;
        color: var(--aca-text) !important;
    }

    .aca-mode-card {
        background: var(--aca-card);
        border: 1px solid var(--aca-border);
        border-radius: var(--aca-radius);
        padding: 1.1rem 1.15rem;
        box-shadow: var(--aca-shadow);
        min-height: 104px;
        transition: border-color 0.15s ease, transform 0.15s ease;
    }

    .aca-mode-card.active {
        border: 2px solid var(--aca-purple);
        background: linear-gradient(180deg, #faf8ff, #f3efff);
        transform: translateY(-1px);
    }

    .aca-mode-card .aca-icon {
        font-size: 1.15rem;
        margin-bottom: 0.35rem;
    }

    .aca-mode-card h4 {
        margin: 0 0 0.35rem 0;
        color: var(--aca-text);
        font-size: 1rem;
    }

    .aca-mode-card p {
        margin: 0;
        color: var(--aca-muted);
        font-size: 0.85rem;
        line-height: 1.35;
    }

    .aca-result-card {
        background: var(--aca-card);
        border: 1px solid var(--aca-border);
        border-radius: var(--aca-radius);
        padding: 1.25rem;
        box-shadow: var(--aca-shadow);
        line-height: 1.6;
    }

    .aca-pro-card {
        background: linear-gradient(145deg, #f5f3ff, #ede9fe);
        border: 1px solid #ddd6fe;
        border-radius: var(--aca-radius);
        padding: 0.95rem;
        margin: 0.75rem 0;
    }

    .aca-login-wrap {
        max-width: 420px;
        margin: 4rem auto 0 auto;
        background: #fff;
        border: 1px solid var(--aca-border);
        border-radius: 18px;
        padding: 1.75rem 1.5rem 1.25rem 1.5rem;
        box-shadow: var(--aca-shadow);
    }

    .aca-login-wrap h2 {
        margin: 0.35rem 0 0.25rem 0;
    }

    .aca-muted { color: var(--aca-muted); font-size: 0.85rem; }
    .aca-brand { font-weight: 700; color: var(--aca-text); }
    .aca-greeting { margin-bottom: 0.15rem; }
</style>
"""
