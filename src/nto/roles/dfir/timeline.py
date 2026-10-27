"""Слияние событий из разных источников в единый таймлайн."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import UTC, datetime
from typing import Any


def parse_timestamp(value: str) -> datetime:
    """Разобрать ISO-8601 с поддержкой суффикса Z."""
    normalized = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed


def merge_timeline(
    events: Iterable[Mapping[str, Any]],
    key: str = "timestamp",
) -> list[dict[str, Any]]:
    """Отсортировать события по времени, сохранив исходные поля."""
    prepared: list[tuple[datetime, dict[str, Any]]] = []
    for event in events:
        if key not in event:
            raise ValueError(f"event without {key!r}: {event!r}")
        moment = event[key]
        if not isinstance(moment, str):
            raise TypeError(f"{key!r} must be a string, got {type(moment).__name__}")
        prepared.append((parse_timestamp(moment), dict(event)))
    prepared.sort(key=lambda pair: pair[0])
    return [event for _, event in prepared]
