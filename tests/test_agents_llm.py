
from hash_audit.agents import AuditState, Evaluator, Corrector
import hash_audit.agents as agents


def test_evaluator_uses_llm(monkeypatch):
    def fake_ollama(prompt, model):
        return "MD5 est trop rapide. Utiliser Argon2id."

    monkeypatch.setattr(agents, "ask_ollama", fake_ollama)

    state = AuditState(
        target="demo.py",
        findings=[
            {"scheme": "md5", "severity": "high"}
        ],
    )

    Evaluator().run(state)

    result = state.trace[-1]

    assert result["agent"] == "evaluateur"
    assert result["model"] == "llama3.2:3b"
    assert "Argon2id" in result["assessment"]


def test_corrector_does_not_apply_patch(monkeypatch):
    def fake_ollama(prompt, model):
        return "Migrer progressivement vers Argon2id."

    monkeypatch.setattr(agents, "ask_ollama", fake_ollama)

    state = AuditState(
        target="demo.py",
        findings=[
            {"scheme": "md5", "severity": "high"}
        ],
    )

    Corrector().run(state)

    result = state.trace[-1]

    assert result["agent"] == "correcteur"
    assert result["model"] == "llama3.2:3b"
    assert result["patch_applied"] is False
    assert "Argon2id" in result["recommendation"]
