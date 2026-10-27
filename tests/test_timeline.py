from __future__ import annotations

import pytest

from nto.roles.dfir.timeline import merge_timeline, parse_timestamp


def test_parse_timestamp_handles_z_suffix():
    parsed = parse_timestamp("2026-11-17T09:00:00Z")
    assert parsed.tzinfo is not None
    assert parsed.hour == 9


def test_parse_timestamp_assumes_utc_for_naive():
    assert parse_timestamp("2026-11-17T09:00:00").tzinfo is not None


def test_merge_timeline_sorts_by_moment():
    events = [
        {"timestamp": "2026-11-17T10:00:00Z", "event": "later"},
        {"timestamp": "2026-11-17T09:00:00Z", "event": "earlier"},
    ]
    merged = merge_timeline(events)
    assert [event["event"] for event in merged] == ["earlier", "later"]


def test_merge_timeline_rejects_missing_key():
    with pytest.raises(ValueError, match="without 'timestamp'"):
        merge_timeline([{"event": "no timestamp"}])


def test_merge_timeline_rejects_non_string_timestamp():
    with pytest.raises(TypeError):
        merge_timeline([{"timestamp": 12345}])
