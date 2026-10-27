"""Разбор XML-вывода nmap в плоский список сервисов.

Файл может быть получен из недоверенной среды, поэтому используем defusedxml.
"""

from __future__ import annotations

from pathlib import Path

from defusedxml import ElementTree as ET


def parse_nmap_xml(path: str | Path) -> list[dict[str, object]]:
    """Вернуть список открытых портов: host, port, protocol, service."""
    root = ET.parse(path).getroot()
    results: list[dict[str, object]] = []
    for host in root.findall("host"):
        address = host.find("address")
        host_ip = address.get("addr", "") if address is not None else ""
        ports = host.find("ports")
        if ports is None:
            continue
        for port in ports.findall("port"):
            state = port.find("state")
            if state is None or state.get("state") != "open":
                continue
            service = port.find("service")
            results.append(
                {
                    "host": host_ip,
                    "port": int(port.get("portid", "0")),
                    "protocol": port.get("protocol", ""),
                    "service": service.get("name", "") if service is not None else "",
                }
            )
    return results
