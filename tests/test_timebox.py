from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from nto.common.timebox import Timebox, parse_duration


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("90s", timedelta(seconds=90)), ("25m", timedelta(minutes=25)), ("2h", timedelta(hours=2))],
)
def test_parse_duration(raw, expected):
    assert parse_duration(raw) == expected


def test_parse_duration_rejects_garbage():
    with pytest.raises(ValueError, match="unsupported duration"):
        parse_duration("25 minutes")


def test_timebox_counts_down():
    start = datetime(2026, 11, 17, 9, 0, tzinfo=UTC)
    box = Timebox(duration=timedelta(minutes=25), started_at=start)
    assert box.remaining(start + timedelta(minutes=5)) == timedelta(minutes=20)
    assert not box.expired(start + timedelta(minutes=24))
    assert box.expired(start + timedelta(minutes=26))
