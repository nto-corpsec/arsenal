"""Поиск и редактирование флагов: чтобы они не утекали в публичные репозитории."""

from __future__ import annotations

import re

FLAG_PATTERN = re.compile(r"(?i)\b(flag|ctf|nto|key)\{[^}\n]{1,200}\}")
PLACEHOLDER = "<redacted>"


def find_flags(text: str) -> list[str]:
    """Вернуть все найденные флаги в порядке появления."""
    return [match.group(0) for match in FLAG_PATTERN.finditer(text)]


def looks_like_flag(value: str) -> bool:
    """Проверить, является ли строка целиком флагом."""
    return bool(FLAG_PATTERN.fullmatch(value.strip()))


def redact(text: str) -> str:
    """Заменить флаги на плейсхолдер."""
    return FLAG_PATTERN.sub(PLACEHOLDER, text)


def contains_flag(text: str) -> bool:
    """Быстрая проверка без извлечения."""
    return FLAG_PATTERN.search(text) is not None
