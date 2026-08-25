"""Backward-compatible prompt export. Prefer prompts.py for new code. """

from prompts import email_prompt, TONES, LENGTHS

__all__ = ["email_prompt", "TONES", "LENGTHS"]
