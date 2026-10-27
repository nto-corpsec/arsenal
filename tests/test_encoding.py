from __future__ import annotations

import pytest

from nto.roles.websec.encoding import b64_encode, hex_encode, url_encode


def test_url_encode_rounds():
    assert url_encode("a b") == "a%20b"
    assert url_encode("a b", rounds=2) == "a%2520b"


def test_url_encode_validates_rounds():
    with pytest.raises(ValueError, match="rounds"):
        url_encode("x", rounds=0)


def test_b64_and_hex():
    assert b64_encode("test") == "dGVzdA=="
    assert hex_encode("AB") == "4142"
