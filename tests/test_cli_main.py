import json

import pytest

from hash_audit import cli


def test_main_dataset_command(tmp_path, monkeypatch):
    output = tmp_path / "accounts.json"
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "sys.argv",
        ["hash-audit", "dataset", "--out", str(output)],
    )

    monkeypatch.setattr(
        cli,
        "generate_accounts",
        lambda: [{"user": "synthetic_0000", "scheme": "md5"}],
    )

    cli.main()

    result = json.loads(output.read_text(encoding="utf-8"))
    assert result[0]["user"] == "synthetic_0000"


def test_main_mutations_command(tmp_path, monkeypatch):
    output = tmp_path / "mutations"
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "sys.argv",
        ["hash-audit", "mutations", "--out", str(output)],
    )

    monkeypatch.setattr(
        cli,
        "generate_mutations",
        lambda: [
            {"id": 0, "mutation": "md5", "code": "import hashlib"},
            {"id": 1, "mutation": "sha1", "code": "hashlib.sha1(b'x')"},
        ],
    )

    cli.main()

    truth = json.loads(
        (output / "ground_truth.json").read_text(encoding="utf-8")
    )

    assert len(truth) == 2
    assert truth[0]["mutation"] == "md5"
    assert "code" not in truth[0]
    assert (output / "target_00.py").read_text(encoding="utf-8") == "import hashlib"


def test_main_migration_command(tmp_path, monkeypatch):
    output = tmp_path / "migration.json"
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "sys.argv",
        ["hash-audit", "migration", "--out", str(output)],
    )

    monkeypatch.setattr(
        cli,
        "simulate_migration",
        lambda: [{"day": 0, "migrated_percent": 33.3}],
    )

    cli.main()

    result = json.loads(output.read_text(encoding="utf-8"))
    assert result == [{"day": 0, "migrated_percent": 33.3}]


def test_main_audit_command_writes_trace(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "sys.argv",
        ["hash-audit", "audit", "target.py"],
    )

    class FakeState:
        findings = [{"scheme": "md5"}]
        trace = [{"agent": "explorateur", "status": "ok"}]

    monkeypatch.setattr(cli, "audit", lambda file: FakeState())

    cli.main()

    trace_path = tmp_path / "traces" / "latest.jsonl"
    lines = trace_path.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 1
    assert json.loads(lines[0])["agent"] == "explorateur"
    assert '"findings"' in capsys.readouterr().out


def test_main_rejects_unknown_command(monkeypatch):
    monkeypatch.setattr("sys.argv", ["hash-audit", "unknown"])

    with pytest.raises(SystemExit) as error:
        cli.main()

    assert error.value.code == 2
