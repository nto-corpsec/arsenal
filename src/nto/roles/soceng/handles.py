"""Варианты написания ника для OSINT-разведки."""

from __future__ import annotations

SEPARATORS = (".", "_", "-")


def handle_variants(handle: str) -> list[str]:
    """Собрать уникальные варианты ника, сохранив исходный первым."""
    cleaned = handle.strip().lstrip("@")
    if not cleaned:
        raise ValueError("handle must not be empty")
    base = cleaned.lower()
    variants = [base]
    for separator in SEPARATORS:
        candidate = f"{base}{separator}"
        if candidate not in variants:
            variants.append(candidate)
    for separator in SEPARATORS:
        stripped = base.replace(separator, "")
        if stripped and stripped not in variants:
            variants.append(stripped)
    return variants
