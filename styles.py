"""Shared SaaS theme CSS for AI Communication Assistant."""

APP_CSS = """
<style>
    :root {
        --aca-purple: #6d28d9;
        --aca-purple-soft: #ede9fe;
        --aca-lavender: #a78bfa;
        --aca-bg: #f8f7fc;
        --aca-card: #ffffff;
        --aca-text: #1e1b4b;
        --aca-muted: #6b7280;
        --aca-radius: 12px;
        --aca-shadow: 0 4px 16px rgba(109, 40, 217, 0.08);
        --aca-border: #e5e7eb;
    }

    .stApp, [data-testid="stAppViewContainer"] {
        background: var(--aca-bg);
        color: var(--aca-text);
    }

    .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 2rem !important;
        max-width: 1100px;
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
        border-radius: 10px !important;
        width: 100%;
        justify-content: flex-start;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: var(--aca-radius) !important;
        border: 1px solid var(--aca-border) !important;
        background: var(--aca-card) !important;
        box-shadow: var(--aca-shadow);
        min-height: 140px;
    }

    div[data-testid="stSelectbox"] > div {
        border-radius: var(--aca-radius) !important;
    }

    div[data-testid="stButton"] > button[kind="primary"] {
        border-radius: var(--aca-radius) !important;
        background: var(--aca-purple) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(109, 40, 217, 0.25);
    }

    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background: #5b21b6 !important;
        color: #ffffff !important;
    }

    div[data-testid="stButton"] > button[kind="secondary"] {
        border-radius: 10px !important;
        border: 1px solid var(--aca-border) !important;
        background: #fff !important;
        color: var(--aca-text) !important;
    }

    .aca-mode-card {
        background: var(--aca-card);
        border: 1px solid var(--aca-border);
        border-radius: var(--aca-radius);
        padding: 1rem 1.1rem;
        box-shadow: var(--aca-shadow);
        min-height: 96px;
    }

    .aca-mode-card.active {
        border: 2px solid var(--aca-purple);
        background: #f5f3ff;
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
    }

    .aca-result-card {
        background: var(--aca-card);
        border: 1px solid var(--aca-border);
        border-radius: var(--aca-radius);
        padding: 1.25rem;
        box-shadow: var(--aca-shadow);
        white-space: pre-wrap;
        line-height: 1.55;
    }

    .aca-pro-card {
        background: linear-gradient(145deg, #f5f3ff, #ede9fe);
        border: 1px solid #ddd6fe;
        border-radius: var(--aca-radius);
        padding: 0.9rem;
        margin: 0.75rem 0;
    }

    .aca-muted { color: var(--aca-muted); font-size: 0.85rem; }
    .aca-brand { font-weight: 700; color: var(--aca-text); }
</style>
"""
