"""Таймбоксы: 25 минут на гипотезу, потом эскалация."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

DURATION_PATTERN = re.compile(r"^(?P<value>\d+)(?P<unit>[smh])$")
_UNIT_SECONDS = {"s": 1, "m": 60, "h": 3600}


def parse_duration(value: str) -> timedelta:
    """Разобрать строку вида 25m, 90s, 2h."""
    match = DURATION_PATTERN.fullmatch(value.strip())
    if match is None:
        raise ValueError(f"unsupported duration: {value!r}")
    return timedelta(seconds=int(match.group("value")) * _UNIT_SECONDS[match.group("unit")])


@dataclass
class Timebox:
    """Обратный отсчёт с моментом старта."""

    duration: timedelta
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def start(cls, value: str) -> Timebox:
        """Создать таймбокс по строке длительности."""
        return cls(duration=parse_duration(value))

    @property
    def deadline(self) -> datetime:
        """Момент истечения."""
        return self.started_at + self.duration

    def remaining(self, now: datetime | None = None) -> timedelta:
        """Сколько осталось; отрицательное значение означает просрочку."""
        current = now or datetime.now(UTC)
        return self.deadline - current

    def expired(self, now: datetime | None = None) -> bool:
        """Истёк ли таймбокс."""
        return self.remaining(now) <= timedelta(0)
