"""SQLite persistence for users, history, and usage tracking."""

from __future__ import annotations

import hashlib
import os
import sqlite3
import time
from pathlib import Path
from typing import Any

# Local: database/aca.db — Cloud-friendly override via ACA_DB_PATH (e.g. /tmp/aca.db)
DB_PATH = Path(os.getenv("ACA_DB_PATH", str(Path(__file__).resolve().parent / "aca.db")))


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                display_name TEXT NOT NULL,
                email TEXT,
                default_tone TEXT DEFAULT 'Professional',
                created_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                feature TEXT NOT NULL,
                title TEXT NOT NULL,
                input_text TEXT,
                output_text TEXT,
                tone TEXT,
                length TEXT,
                created_at REAL NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS usage_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                feature TEXT NOT NULL,
                model TEXT,
                input_tokens INTEGER DEFAULT 0,
                output_tokens INTEGER DEFAULT 0,
                total_tokens INTEGER DEFAULT 0,
                latency_ms INTEGER DEFAULT 0,
                status TEXT NOT NULL,
                created_at REAL NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            """
        )


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def ensure_demo_user() -> None:
    """Create a demo account for local/cloud learning use."""
    with _connect() as conn:
        row = conn.execute("SELECT id FROM users WHERE username = ?", ("demo",)).fetchone()
        if row:
            return
        conn.execute(
            """
            INSERT INTO users (username, password_hash, display_name, email, default_tone, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "demo",
                hash_password("demo123"),
                "Muhamad Waqas",
                "muhamad@example.com",
                "Professional",
                time.time(),
            ),
        )


def authenticate(username: str, password: str) -> dict[str, Any] | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password_hash = ?",
            (username.strip().lower(), hash_password(password)),
        ).fetchone()
        return dict(row) if row else None


def username_exists(username: str) -> bool:
    with _connect() as conn:
        row = conn.execute(
            "SELECT id FROM users WHERE username = ?",
            (username.strip().lower(),),
        ).fetchone()
        return row is not None


def create_user(
    *,
    username: str,
    password: str,
    display_name: str,
    email: str = "",
) -> tuple[dict[str, Any] | None, str]:
    """Create a user account. Returns (user, error_message)."""
    username = username.strip().lower()
    display_name = display_name.strip()
    email = email.strip()

    if len(username) < 3:
        return None, "Username must be at least 3 characters."
    if not username.replace("_", "").isalnum():
        return None, "Username can only contain letters, numbers, and underscores."
    if len(password) < 6:
        return None, "Password must be at least 6 characters."
    if not display_name:
        return None, "Please enter your display name."
    if username_exists(username):
        return None, "That username is already taken."

    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO users (username, password_hash, display_name, email, default_tone, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                username,
                hash_password(password),
                display_name,
                email,
                "Professional",
                time.time(),
            ),
        )
        user_id = int(cur.lastrowid)

    return get_user(user_id), ""


def get_user(user_id: int | str) -> dict[str, Any] | None:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


def update_profile(user_id: int | str, display_name: str, email: str, default_tone: str) -> None:
    with _connect() as conn:
        conn.execute(
            """
            UPDATE users
            SET display_name = ?, email = ?, default_tone = ?
            WHERE id = ?
            """,
            (display_name.strip(), email.strip(), default_tone, user_id),
        )


def add_history(
    *,
    user_id: int | str,
    feature: str,
    title: str,
    input_text: str,
    output_text: str,
    tone: str,
    length: str,
) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO history (user_id, feature, title, input_text, output_text, tone, length, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, feature, title[:80], input_text, output_text, tone, length, time.time()),
        )


def list_history(user_id: int | str, limit: int = 8) -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT id, feature, title, created_at
            FROM history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]


def get_history_item(user_id: int | str, item_id: int) -> dict[str, Any] | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM history WHERE id = ? AND user_id = ?",
            (item_id, user_id),
        ).fetchone()
        return dict(row) if row else None


def estimate_tokens(text: str) -> int:
    # Rough heuristic for learning/demo usage tracking (~4 chars per token).
    return max(1, len(text) // 4) if text else 0


def add_usage(
    *,
    user_id: int | str | None,
    feature: str,
    model: str,
    input_text: str,
    output_text: str,
    latency_ms: int,
    status: str,
) -> None:
    in_tok = estimate_tokens(input_text)
    out_tok = estimate_tokens(output_text)
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO usage_events (
                user_id, feature, model, input_tokens, output_tokens, total_tokens,
                latency_ms, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                feature,
                model,
                in_tok,
                out_tok,
                in_tok + out_tok,
                latency_ms,
                status,
                time.time(),
            ),
        )


def usage_summary(user_id: int | str) -> dict[str, int]:
    with _connect() as conn:
        row = conn.execute(
            """
            SELECT
                COUNT(*) AS requests,
                COALESCE(SUM(total_tokens), 0) AS tokens
            FROM usage_events
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()
        return {"requests": int(row["requests"]), "tokens": int(row["tokens"])}
