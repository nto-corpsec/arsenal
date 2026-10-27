"""Кодирование пейлоадов для веб-задач."""

from __future__ import annotations

import base64
from urllib.parse import quote


def url_encode(value: str, rounds: int = 1) -> str:
    """URL-кодирование, при необходимости многократное."""
    if rounds < 1:
        raise ValueError("rounds must be >= 1")
    result = value
    for _ in range(rounds):
        result = quote(result, safe="")
    return result


def b64_encode(value: str) -> str:
    """Base64 без переносов строк."""
    return base64.b64encode(value.encode("utf-8")).decode("ascii")


def hex_encode(value: str) -> str:
    """Шестнадцатеричное представление UTF-8."""
    return value.encode("utf-8").hex()
