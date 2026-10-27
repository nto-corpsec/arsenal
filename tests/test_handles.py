from __future__ import annotations

import pytest

from nto.roles.soceng.handles import handle_variants


def test_handle_variants_keeps_original_first():
    variants = handle_variants("@Analyst")
    assert variants[0] == "analyst"
    assert "analyst." in variants
    assert "analyst_" in variants


def test_handle_variants_are_unique():
    variants = handle_variants("a")
    assert len(variants) == len(set(variants))


def test_handle_variants_rejects_empty():
    with pytest.raises(ValueError, match="empty"):
        handle_variants("@")
