from __future__ import annotations

import hashlib

from nto.cli import main


def test_cli_hash_prints_digest(tmp_path, capsys):
    target = tmp_path / "evidence.txt"
    target.write_bytes(b"chain-of-custody")
    assert main(["hash", str(target)]) == 0
    assert capsys.readouterr().out.strip() == hashlib.sha256(b"chain-of-custody").hexdigest()


def test_cli_manifest_writes_file(tmp_path, capsys):
    target = tmp_path / "a.txt"
    target.write_text("a", encoding="utf-8")
    output = tmp_path / "manifest.json"
    assert main(["manifest", str(target), "-o", str(output)]) == 0
    assert output.exists()
    assert str(output) in capsys.readouterr().out


def test_cli_scan_flags_returns_one_on_hit(tmp_path):
    target = tmp_path / "note.txt"
    target.write_text("nto{found}", encoding="utf-8")
    assert main(["scan-flags", str(target)]) == 1


def test_cli_scan_flags_returns_zero_when_clean(tmp_path, capsys):
    target = tmp_path / "note.txt"
    target.write_text("nothing here", encoding="utf-8")
    assert main(["scan-flags", str(target)]) == 0
    assert capsys.readouterr().out == ""
