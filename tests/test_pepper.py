from hash_audit.crypto import (
    get_configured_pepper,
    hash_password,
    migrate_on_login,
    verify_password,
)


def test_pepper_hash_verification():
    password = "Demo-Password-2026!"
    pepper = "Secret-Pepper-Test"

    stored = hash_password(password, pepper=pepper)

    assert stored.startswith("$argon2id$")
    assert verify_password(stored, password, pepper=pepper)


def test_wrong_pepper_is_rejected():
    stored = hash_password("Demo-Password-2026!", pepper="Pepper-A")

    assert not verify_password(
        stored,
        "Demo-Password-2026!",
        pepper="Pepper-B"
    )


def test_missing_pepper_is_rejected():
    stored = hash_password("Demo-Password-2026!", pepper="Secret-Pepper")

    assert not verify_password(stored, "Demo-Password-2026!")


def test_password_without_pepper_remains_compatible():
    password = "Demo-Password-2026!"
    stored = hash_password(password)

    assert verify_password(stored, password)


def test_pepper_is_loaded_from_environment(monkeypatch):
    monkeypatch.setenv("HASH_AUDIT_PEPPER", "Environment-Secret")

    assert get_configured_pepper() == "Environment-Secret"


def test_empty_environment_pepper_returns_none(monkeypatch):
    monkeypatch.delenv("HASH_AUDIT_PEPPER", raising=False)

    assert get_configured_pepper() is None



def test_migrate_md5_to_argon2id_with_pepper():
    password = "Demo-Password-2026!"
    old_hash = hash_password(password, scheme="md5")

    success, new_hash = migrate_on_login(
        old_hash,
        password,
        pepper="New-Secret-Pepper"
    )

    assert success
    assert new_hash.startswith("$argon2id$")
    assert verify_password(
        new_hash,
        password,
        pepper="New-Secret-Pepper"
    )


def test_migrate_legacy_argon2id_to_pepper():
    password = "Demo-Password-2026!"
    old_hash = hash_password(password)

    success, new_hash = migrate_on_login(
        old_hash,
        password,
        pepper="New-Secret-Pepper"
    )

    assert success
    assert new_hash != old_hash
    assert verify_password(
        new_hash,
        password,
        pepper="New-Secret-Pepper"
    )


def test_existing_peppered_argon2id_is_preserved():
    password = "Demo-Password-2026!"
    pepper = "Secret-Pepper"
    old_hash = hash_password(password, pepper=pepper)

    success, new_hash = migrate_on_login(
        old_hash,
        password,
        pepper=pepper
    )

    assert success
    assert new_hash == old_hash


def test_migration_rejects_wrong_password():
    old_hash = hash_password("Correct-Password", scheme="md5")

    success, new_hash = migrate_on_login(
        old_hash,
        "Wrong-Password",
        pepper="Secret-Pepper"
    )

    assert not success
    assert new_hash == old_hash


def test_migration_rejects_wrong_pepper():
    password = "Demo-Password-2026!"
    old_hash = hash_password(password, pepper="Pepper-A")

    success, new_hash = migrate_on_login(
        old_hash,
        password,
        pepper="Pepper-B"
    )

    assert not success
    assert new_hash == old_hash
