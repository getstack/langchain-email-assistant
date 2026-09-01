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
        /* Keep greeting below Streamlit's top toolbar so it is not clipped */
        padding-top: 4rem !important;
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
        min-width: 300px !important;
        width: 300px !important;
    }

    section[data-testid="stSidebar"] > div:first-child {
        width: 300px !important;
    }

    section[data-testid="stSidebar"] .stButton > button {
        border-radius: 12px !important;
        width: 100%;
        justify-content: flex-start;
        font-weight: 500 !important;
        white-space: normal !important;
        text-align: left !important;
        height: auto !important;
        min-height: 2.5rem;
        line-height: 1.3 !important;
    }

    /* Compact RECENT history rows (match mockup) */
    .aca-recent-row {
        display: flex;
        align-items: flex-start;
        gap: 0.45rem;
        padding: 0.35rem 0.4rem;
        border-radius: 8px;
        margin: 0 0 0.15rem 0;
        min-height: 2.2rem;
    }

    .aca-recent-row:hover {
        background: var(--aca-purple-soft);
    }

    .aca-recent-icon {
        font-size: 0.85rem;
        line-height: 1.3;
        flex-shrink: 0;
        margin-top: 0.05rem;
    }

    .aca-recent-text {
        min-width: 0;
        flex: 1;
    }

    .aca-recent-title {
        color: var(--aca-text);
        font-size: 0.8rem;
        font-weight: 600;
        line-height: 1.2;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .aca-recent-time {
        color: var(--aca-muted);
        font-size: 0.68rem;
        line-height: 1.15;
        margin-top: 0.1rem;
    }

    section[data-testid="stSidebar"] button[kind="tertiary"] {
        min-height: 1.8rem !important;
        height: 1.8rem !important;
        padding: 0 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        color: var(--aca-muted) !important;
        justify-content: center !important;
    }

    section[data-testid="stSidebar"] button[kind="tertiary"]:hover {
        background: var(--aca-purple-soft) !important;
        color: var(--aca-purple) !important;
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

    /* ---- Auth card (sign in / sign up) ---- */
    .aca-auth-brand {
        margin-bottom: 0.75rem;
    }

    .aca-auth-brand h2 {
        margin: 0.4rem 0 0.25rem 0 !important;
        color: var(--aca-text) !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }

    .aca-demo-hint {
        color: var(--aca-muted);
        font-size: 0.85rem;
        margin: 0 0 0.75rem 0;
    }

    .aca-demo-hint code {
        background: var(--aca-purple-soft);
        color: var(--aca-purple);
        padding: 0.1rem 0.35rem;
        border-radius: 6px;
        font-size: 0.8rem;
    }

    /* Auth text inputs: ONE clean border — no inset purple ring */
    [data-testid="stTextInput"] > div > div {
        border: 1px solid var(--aca-border) !important;
        border-radius: 12px !important;
        background: #faf9ff !important;
        box-shadow: none !important;
    }

    [data-testid="stTextInput"] > div > div:focus-within {
        border-color: var(--aca-lavender) !important;
        box-shadow: 0 0 0 1px var(--aca-lavender) !important;
    }

    [data-testid="stTextInput"] input {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        background: transparent !important;
        padding-right: 0.75rem !important;
    }

    [data-testid="stTextInput"] input:focus {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }

    /* Hide Streamlit password eye + enter/apply hint (they collide) */
    [data-testid="stTextInput"] button,
    [data-testid="stTextInput"] [data-testid="stBaseButton-secondary"],
    [data-testid="InputInstructions"],
    [data-testid="stTextInput"] [data-testid="InputInstructions"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        position: absolute !important;
        left: -10000px !important;
    }

    /* Purple primary buttons (Sign in / Create account) */
    button[kind="primary"],
    button[data-testid="baseButton-primary"] {
        border-radius: var(--aca-radius) !important;
        background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
        background-color: #6d28d9 !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 18px rgba(109, 40, 217, 0.28) !important;
    }

    button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover {
        background: #5b21b6 !important;
        background-color: #5b21b6 !important;
        color: #ffffff !important;
    }

    .aca-muted { color: var(--aca-muted); font-size: 0.85rem; }
    .aca-brand { font-weight: 700; color: var(--aca-text); }
    .aca-greeting {
        margin-top: 0.25rem;
        margin-bottom: 0.15rem;
        line-height: 1.25;
    }
</style>
"""
