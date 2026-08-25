"""Production helpers: validation, rate limiting, logging."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

logger = logging.getLogger("aca")


def configure_logging() -> None:
    if logger.handlers:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


@dataclass
class ValidationResult:
    ok: bool
    message: str = ""


def validate_text(value: str, *, field: str, min_len: int = 1, max_len: int = 4000) -> ValidationResult:
    text = (value or "").strip()
    if len(text) < min_len:
        return ValidationResult(False, f"Please enter {field} before generating.")
    if len(text) > max_len:
        return ValidationResult(False, f"{field.capitalize()} must be at most {max_len} characters.")
    return ValidationResult(True)


class RateLimiter:
    """Simple in-memory rate limiter per user/session key."""

    def __init__(self, max_calls: int = 20, window_seconds: int = 60):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._hits: dict[str, list[float]] = {}

    def allow(self, key: str) -> tuple[bool, str]:
        now = time.time()
        bucket = self._hits.setdefault(key, [])
        self._hits[key] = [t for t in bucket if now - t < self.window_seconds]
        if len(self._hits[key]) >= self.max_calls:
            return False, "Rate limit reached. Please wait a minute and try again."
        self._hits[key].append(now)
        return True, ""


rate_limiter = RateLimiter()
