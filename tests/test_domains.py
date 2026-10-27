from __future__ import annotations

import pytest

from nto.roles.osint.domains import normalize_host, registrable_domain


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("https://Example.COM:8443/path?q=1", "example.com"),
        ("sub.example.org.", "sub.example.org"),
        ("  mail.example.net  ", "mail.example.net"),
    ],
)
def test_normalize_host(raw, expected):
    assert normalize_host(raw) == expected


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("news.example.co.uk", "example.co.uk"),
        ("a.b.example.com", "example.com"),
        ("example.com", "example.com"),
        ("localhost", "localhost"),
    ],
)
def test_registrable_domain(raw, expected):
    assert registrable_domain(raw) == expected
