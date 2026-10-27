from __future__ import annotations

import hashlib
import json

from nto.common.artifacts import build_manifest, sha256_file, write_manifest


def test_sha256_matches_hashlib(tmp_path):
    payload = b"corpsec" * 1000
    target = tmp_path / "sample.bin"
    target.write_bytes(payload)
    assert sha256_file(target) == hashlib.sha256(payload).hexdigest()


def test_manifest_contains_size_and_digest(tmp_path):
    target = tmp_path / "artifact.txt"
    target.write_text("evidence", encoding="utf-8")
    manifest = build_manifest([target])
    assert manifest[0]["path"].endswith("artifact.txt")
    assert manifest[0]["size"] == 8
    assert len(str(manifest[0]["sha256"])) == 64


def test_write_manifest_is_valid_json(tmp_path):
    first = tmp_path / "a.txt"
    second = tmp_path / "b.txt"
    first.write_text("a", encoding="utf-8")
    second.write_text("bb", encoding="utf-8")
    output = tmp_path / "out" / "manifest.json"
    write_manifest([first, second], output)
    parsed = json.loads(output.read_text(encoding="utf-8"))
    assert [entry["size"] for entry in parsed] == [1, 2]
