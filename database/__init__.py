"""Supabase persistence for history and usage tracking."""

from __future__ import annotations

import time
from datetime import datetime
from typing import Any

from auth.supabase_client import get_supabase_client


def _parse_ts(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    return time.time()


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4) if text else 0


def add_history(
    *,
    user_id: str,
    feature: str,
    title: str,
    input_text: str,
    output_text: str,
    tone: str,
    length: str,
) -> None:
    client = get_supabase_client()
    client.table("history").insert(
        {
            "user_id": user_id,
            "feature": feature,
            "title": (title or feature)[:80],
            "input_text": input_text,
            "output_text": output_text,
            "tone": tone,
            "length": length,
        }
    ).execute()


def list_history(user_id: str, limit: int = 8) -> list[dict[str, Any]]:
    client = get_supabase_client()
    res = (
        client.table("history")
        .select("id, feature, title, created_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    items: list[dict[str, Any]] = []
    for row in res.data or []:
        items.append(
            {
                "id": row["id"],
                "feature": row["feature"],
                "title": row["title"],
                "created_at": _parse_ts(row.get("created_at")),
            }
        )
    return items


def get_history_item(user_id: str, item_id: int) -> dict[str, Any] | None:
    client = get_supabase_client()
    res = (
        client.table("history")
        .select("*")
        .eq("id", item_id)
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    rows = res.data or []
    if not rows:
        return None
    row = rows[0]
    row["created_at"] = _parse_ts(row.get("created_at"))
    return row


def add_usage(
    *,
    user_id: str | None,
    feature: str,
    model: str,
    input_text: str,
    output_text: str,
    latency_ms: int,
    status: str,
) -> None:
    if not user_id:
        return
    in_tok = estimate_tokens(input_text)
    out_tok = estimate_tokens(output_text)
    client = get_supabase_client()
    client.table("usage_events").insert(
        {
            "user_id": user_id,
            "feature": feature,
            "model": model,
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "total_tokens": in_tok + out_tok,
            "latency_ms": latency_ms,
            "status": status,
        }
    ).execute()


def usage_summary(user_id: str) -> dict[str, int]:
    client = get_supabase_client()
    res = (
        client.table("usage_events")
        .select("total_tokens")
        .eq("user_id", user_id)
        .execute()
    )
    rows = res.data or []
    return {
        "requests": len(rows),
        "tokens": sum(int(r.get("total_tokens") or 0) for r in rows),
    }
