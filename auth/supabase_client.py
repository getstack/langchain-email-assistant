"""Supabase client factory."""

from __future__ import annotations

from functools import lru_cache

from config import supabase_anon_key, supabase_enabled, supabase_url


@lru_cache(maxsize=1)
def get_supabase_client():
    if not supabase_enabled():
        raise RuntimeError("Supabase is not configured. Set SUPABASE_URL and SUPABASE_ANON_KEY.")
    from supabase import create_client

    return create_client(supabase_url(), supabase_anon_key())
