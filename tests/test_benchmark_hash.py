from hash_audit.benchmark_hash import (
    benchmark_argon2,
    benchmark_scrypt,
    benchmark_bcrypt,
    benchmark_pbkdf2,
    run_benchmark,
)


def test_argon2_benchmark_verifies_password():
    _, verify = benchmark_argon2("Test-Password-2026!")
    assert verify("Test-Password-2026!") is True


def test_scrypt_benchmark_verifies_password():
    _, verify = benchmark_scrypt("Test-Password-2026!")
    assert verify("Test-Password-2026!") is True
    assert verify("Wrong-Password") is False


def test_bcrypt_benchmark_verifies_password():
    _, verify = benchmark_bcrypt("Test-Password-2026!")
    assert verify("Test-Password-2026!") is True
    assert verify("Wrong-Password") is False


def test_pbkdf2_benchmark_verifies_password():
    _, verify = benchmark_pbkdf2("Test-Password-2026!")
    assert verify("Test-Password-2026!") is True
    assert verify("Wrong-Password") is False


def test_run_benchmark_returns_expected_results(monkeypatch):
    import hash_audit.benchmark_hash as benchmark

    def fake_algorithm(password):
        return "fake-hash", lambda candidate: candidate == password

    monkeypatch.setattr(benchmark, "ALGORITHMS", {
        "TestAlgorithm": fake_algorithm,
    })
    monkeypatch.setattr(benchmark, "REPETITIONS", 2)

    results = run_benchmark()

    assert len(results) == 1
    assert results[0]["algorithm"] == "TestAlgorithm"
    assert results[0]["repetitions"] == 2
    assert results[0]["verification"] == "success"
    assert results[0]["hash_ms"] >= 0
    assert results[0]["verify_ms"] >= 0
