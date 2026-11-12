import json

from hash_audit.cli import audit_batch


def test_audit_batch_detects_md5(tmp_path):
    (tmp_path / "target_00.py").write_text(
        "import hashlib\n"
        "digest = hashlib.md5(password.encode()).hexdigest()\n",
        encoding="utf-8",
    )

    (tmp_path / "ground_truth.json").write_text(
        json.dumps([{"id": 0, "mutation": "md5"}]),
        encoding="utf-8",
    )

    output = tmp_path / "report.json"
    audit_batch(str(tmp_path), str(output))

    report = json.loads(output.read_text(encoding="utf-8"))

    assert report["summary"]["total"] == 1
    assert report["summary"]["audited"] == 1
    assert report["summary"]["matched"] == 1
    assert report["results"][0]["detected"] is True
    assert report["summary"]["llm_enabled"] is False


def test_audit_batch_handles_missing_file(tmp_path):
    (tmp_path / "ground_truth.json").write_text(
        json.dumps([{"id": 0, "mutation": "md5"}]),
        encoding="utf-8",
    )

    output = tmp_path / "report.json"
    audit_batch(str(tmp_path), str(output))

    report = json.loads(output.read_text(encoding="utf-8"))

    assert report["summary"]["total"] == 1
    assert report["summary"]["audited"] == 0
    assert report["summary"]["matched"] == 0
    assert report["results"][0]["error"] == "Fichier absent"


def test_audit_batch_handles_empty_dataset(tmp_path):
    (tmp_path / "ground_truth.json").write_text(
        "[]",
        encoding="utf-8",
    )

    output = tmp_path / "report.json"
    audit_batch(str(tmp_path), str(output))

    report = json.loads(output.read_text(encoding="utf-8"))

    assert report["summary"]["total"] == 0
    assert report["summary"]["matched"] == 0
    assert report["summary"]["detection_rate_percent"] == 0
