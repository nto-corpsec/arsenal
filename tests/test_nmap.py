from __future__ import annotations

from pathlib import Path

from nto.roles.netsec.nmap import parse_nmap_xml

FIXTURE = Path(__file__).parent / "fixtures" / "nmap.xml"


def test_parse_nmap_returns_only_open_ports():
    ports = parse_nmap_xml(FIXTURE)
    assert [entry["port"] for entry in ports] == [22, 443]


def test_parse_nmap_keeps_service_and_host():
    ports = parse_nmap_xml(FIXTURE)
    assert ports[0]["host"] == "10.0.0.5"
    assert ports[1]["service"] == "https"
    assert ports[0]["protocol"] == "tcp"
