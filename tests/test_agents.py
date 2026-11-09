from hash_audit.agents import audit
from hash_audit.dataset import generate_accounts,generate_mutations,simulate_migration

def test_agents(tmp_path):
    file=tmp_path/"target.py";file.write_text("import hashlib\nx = hashlib.md5(b'hello').hexdigest()\n")
    result=audit(str(file))
    assert len(result.trace)==6
    assert any(f["scheme"]=="md5" for f in result.findings)

def test_reject_untrusted_file(tmp_path):
    file=tmp_path/"x.csv";file.write_text("hello")
    import pytest
    with pytest.raises(ValueError):audit(str(file))

def test_dataset():
    assert len(generate_accounts())==1000
    assert len(generate_mutations())==25
    curve=simulate_migration()
    assert len(curve)==91
    assert curve[-1]["migrated_percent"]>=curve[0]["migrated_percent"]
