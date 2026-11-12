from hash_audit.crypto import hash_password
from hash_audit.dictionary_attack import run_dictionary_attack


def test_dictionary_attack_md5():
    stored = hash_password("Demo-123456-!", "md5")
    result = run_dictionary_attack(
        stored,
        ["incorrect", "Demo-123456-!", "autre"]
    )
    assert result["success"] is True
    assert result["recovered_password"] == "Demo-123456-!"
    assert result["attempts"] == 2


def test_dictionary_attack_sha256_salted():
    stored = hash_password("Demo-123456-!", "sha256_salted")
    result = run_dictionary_attack(
        stored,
        ["incorrect", "Demo-123456-!"]
    )
    assert result["success"] is True
    assert result["scheme"] == "sha256_salted"


def test_dictionary_attack_argon2id():
    stored = hash_password("Demo-123456-!", "argon2id")
    result = run_dictionary_attack(
        stored,
        ["incorrect", "Demo-123456-!"]
    )
    assert result["success"] is True
    assert result["scheme"] == "argon2id"


def test_dictionary_attack_not_found():
    stored = hash_password("Demo-123456-!", "md5")
    result = run_dictionary_attack(stored, ["incorrect", "unknown"])
    assert result["success"] is False
    assert result["recovered_password"] is None
    assert result["attempts"] == 2


def test_dictionary_attack_unknown_hash():
    try:
        run_dictionary_attack("invalid-hash", ["test"])
        assert False, "Une erreur était attendue."
    except ValueError:
        pass
