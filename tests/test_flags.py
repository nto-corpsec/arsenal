from __future__ import annotations

from nto.common.flags import contains_flag, find_flags, looks_like_flag, redact


def test_find_flags_returns_matches():
    text = "first nto{alpha} then flag{beta_gamma}"
    assert find_flags(text) == ["nto{alpha}", "flag{beta_gamma}"]


def test_find_flags_is_case_insensitive():
    assert find_flags("FLAG{upper}") == ["FLAG{upper}"]


def test_looks_like_flag_requires_full_match():
    assert looks_like_flag("  ctf{ok}  ")
    assert not looks_like_flag("prefix ctf{ok}")


def test_redact_replaces_with_placeholder():
    assert redact("answer is key{secret}") == "answer is <redacted>"
    assert "<redacted>" not in redact("no flags here")


def test_contains_flag_boolean():
    assert contains_flag("x key{1} y")
    assert not contains_flag("x keyboard y")
