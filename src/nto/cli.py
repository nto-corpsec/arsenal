"""CLI команды: nto hash | manifest | scan-flags | redact | timebox."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from nto.common.artifacts import sha256_file, write_manifest
from nto.common.flags import find_flags, redact
from nto.common.timebox import Timebox


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nto", description="Инструменты команды НТО CorpSec")
    subparsers = parser.add_subparsers(dest="command", required=True)

    hash_parser = subparsers.add_parser("hash", help="посчитать SHA-256 файла")
    hash_parser.add_argument("path", type=Path)

    manifest_parser = subparsers.add_parser("manifest", help="собрать JSON-манифест артефактов")
    manifest_parser.add_argument("paths", nargs="+", type=Path)
    manifest_parser.add_argument("-o", "--output", type=Path, default=Path("manifest.json"))

    scan_parser = subparsers.add_parser("scan-flags", help="найти флаги в файле или stdin")
    scan_parser.add_argument("path", nargs="?", type=Path)

    subparsers.add_parser("redact", help="замаскировать флаги в stdin")

    timebox_parser = subparsers.add_parser("timebox", help="запустить таймбокс")
    timebox_parser.add_argument("duration", help="например 25m")

    return parser


def _read_text(path: Path | None) -> str:
    if path is None:
        return sys.stdin.read()
    return path.read_text(encoding="utf-8", errors="replace")


def main(argv: Sequence[str] | None = None) -> int:
    """Точка входа CLI."""
    args = _build_parser().parse_args(argv)

    if args.command == "hash":
        print(sha256_file(args.path))
        return 0

    if args.command == "manifest":
        destination = write_manifest(args.paths, args.output)
        print(destination)
        return 0

    if args.command == "scan-flags":
        found = find_flags(_read_text(args.path))
        for flag in found:
            print(flag)
        return 1 if found else 0

    if args.command == "redact":
        sys.stdout.write(redact(sys.stdin.read()))
        return 0

    if args.command == "timebox":
        box = Timebox.start(args.duration)
        print(f"deadline: {box.deadline.isoformat()}")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
