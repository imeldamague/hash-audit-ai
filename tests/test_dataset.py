from collections import Counter

from hash_audit.crypto import verify_password
from hash_audit.dataset import (
    generate_accounts,
    generate_password_candidates,
)


def test_candidates_are_reproducible():
    assert generate_password_candidates() == generate_password_candidates()


def test_accounts_have_no_plaintext_passwords():
    accounts = generate_accounts(6, pepper="Test-Pepper-2026")

    assert len(accounts) == 6
    assert all("password" not in account for account in accounts)
    assert all(account.get("password_hash") for account in accounts)
    assert all(set(account) == {"user", "scheme", "password_hash"} for account in accounts)


def test_accounts_have_expected_scheme_distribution():
    accounts = generate_accounts(6, pepper="Test-Pepper-2026")
    distribution = Counter(account["scheme"] for account in accounts)

    assert distribution == {
        "md5": 2,
        "sha256_salted": 2,
        "argon2id": 2,
    }


def test_generated_hashes_match_reproducible_candidates():
    pepper = "Test-Pepper-2026"
    accounts = generate_accounts(6, pepper=pepper)
    candidates = generate_password_candidates(6)

    for account, password in zip(accounts, candidates):
        account_pepper = pepper if account["scheme"] == "argon2id" else None

        assert verify_password(
            account["password_hash"],
            password,
            pepper=account_pepper,
        )



def test_migration_simulation_is_reproducible():
    from hash_audit.dataset import simulate_migration

    assert simulate_migration() == simulate_migration()


def test_migration_simulation_has_91_daily_points():
    from hash_audit.dataset import simulate_migration

    result = simulate_migration(n=1000, days=90)

    assert len(result) == 91
    assert result[0]["day"] == 0
    assert result[-1]["day"] == 90


def test_migration_simulation_is_monotonic_and_bounded():
    from hash_audit.dataset import simulate_migration

    result = simulate_migration(n=1000, days=90)
    percentages = [item["migrated_percent"] for item in result]

    assert all(0 <= value <= 100 for value in percentages)
    assert all(
        percentages[i] <= percentages[i + 1]
        for i in range(len(percentages) - 1)
    )


def test_migration_simulation_supports_custom_parameters():
    from hash_audit.dataset import simulate_migration

    result = simulate_migration(n=100, days=30)

    assert len(result) == 31
    assert result[0]["migrated_percent"] == 33.0
    assert result[-1]["day"] == 30
