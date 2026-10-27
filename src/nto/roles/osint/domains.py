"""Нормализация хостов и выделение registrable domain без внешних зависимостей."""

from __future__ import annotations

from urllib.parse import urlsplit

SECOND_LEVEL_SUFFIXES = frozenset(
    {
        "co.uk",
        "org.uk",
        "ac.uk",
        "com.au",
        "net.au",
        "co.jp",
        "co.nz",
        "com.br",
        "co.in",
        "msk.ru",
        "spb.ru",
    }
)


def normalize_host(value: str) -> str:
    """Привести URL или хост к нижнему регистру без схемы, порта и точки."""
    candidate = value.strip()
    if "://" in candidate:
        candidate = urlsplit(candidate).hostname or ""
    else:
        candidate = candidate.split("/")[0]
        candidate = candidate.split(":")[0]
    return candidate.rstrip(".").lower()


def registrable_domain(value: str) -> str:
    """Выделить eTLD+1: news.example.co.uk -> example.co.uk."""
    host = normalize_host(value)
    labels = [label for label in host.split(".") if label]
    if len(labels) <= 2:
        return ".".join(labels)
    suffix = ".".join(labels[-2:])
    if suffix in SECOND_LEVEL_SUFFIXES and len(labels) >= 3:
        return ".".join(labels[-3:])
    return suffix
