"""Хеширование и манифесты артефактов для chain of custody."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path

CHUNK_SIZE = 1024 * 1024


@dataclass(frozen=True)
class Artifact:
    """Описание файла: путь, размер и SHA-256."""

    path: str
    size: int
    sha256: str

    def to_dict(self) -> dict[str, object]:
        """Сериализуемое представление."""
        return asdict(self)


def sha256_file(path: str | Path) -> str:
    """Посчитать SHA-256 файла потоком."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def describe(path: str | Path) -> Artifact:
    """Собрать описание артефакта."""
    candidate = Path(path)
    return Artifact(
        path=str(candidate), size=candidate.stat().st_size, sha256=sha256_file(candidate)
    )


def build_manifest(paths: Iterable[str | Path]) -> list[dict[str, object]]:
    """Собрать манифест по списку путей."""
    return [describe(path).to_dict() for path in paths]


def write_manifest(paths: Iterable[str | Path], destination: str | Path) -> Path:
    """Записать манифест в JSON-файл и вернуть путь."""
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(build_manifest(paths), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return target
