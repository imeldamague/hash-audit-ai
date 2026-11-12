import app.demo as demo


def setup_function():
    demo.USERS.clear()
    demo.PEPPER = None
    demo.SCHEME = "md5"
    demo.BREACH_CHECK_ENABLED = False


def test_register_and_login_migrates_md5_to_argon2id():
    client = demo.app.test_client()

    response = client.post(
        "/register",
        json={"username": "alice", "password": "Demo-Password-2026!"}
    )

    assert response.status_code == 201
    assert demo.USERS["alice"][:4] != "$arg"

    response = client.post(
        "/login",
        json={"username": "alice", "password": "Demo-Password-2026!"}
    )

    assert response.status_code == 200
    assert response.json["ok"] is True
    assert response.json["migrated"] is True
    assert response.json["scheme"] == "argon2id"


def test_login_migrates_md5_to_argon2id_with_pepper():
    client = demo.app.test_client()
    demo.PEPPER = "Test-Application-Pepper"

    client.post(
        "/register",
        json={"username": "bob", "password": "Demo-Password-2026!"}
    )

    response = client.post(
        "/login",
        json={"username": "bob", "password": "Demo-Password-2026!"}
    )

    assert response.status_code == 200
    assert response.json["migrated"] is True

    stored = demo.USERS["bob"]

    assert stored.startswith("$argon2id$")
    assert demo.verify_password(
        stored,
        "Demo-Password-2026!",
        pepper=demo.PEPPER
    )


def test_second_login_does_not_migrate_again():
    client = demo.app.test_client()
    demo.PEPPER = "Test-Application-Pepper"

    client.post(
        "/register",
        json={"username": "carol", "password": "Demo-Password-2026!"}
    )

    client.post(
        "/login",
        json={"username": "carol", "password": "Demo-Password-2026!"}
    )

    response = client.post(
        "/login",
        json={"username": "carol", "password": "Demo-Password-2026!"}
    )

    assert response.status_code == 200
    assert response.json["ok"] is True
    assert response.json["migrated"] is False


def test_wrong_password_does_not_migrate():
    client = demo.app.test_client()

    client.post(
        "/register",
        json={"username": "david", "password": "Correct-Password"}
    )

    old_hash = demo.USERS["david"]

    response = client.post(
        "/login",
        json={"username": "david", "password": "Wrong-Password"}
    )

    assert response.status_code == 401
    assert demo.USERS["david"] == old_hash



def test_register_rejects_compromised_password(monkeypatch):
    demo.BREACH_CHECK_ENABLED = True
    monkeypatch.setattr(
        demo,
        "check_password_breach",
        lambda password: {
            "status": "compromised",
            "compromised": True,
            "count": 42,
        },
    )

    response = demo.app.test_client().post(
        "/register",
        json={"username": "eve", "password": "Compromised-Password"},
    )

    assert response.status_code == 400
    assert response.json["occurrences"] == 42
    assert "eve" not in demo.USERS


def test_register_fails_closed_when_breach_api_unavailable(monkeypatch):
    demo.BREACH_CHECK_ENABLED = True
    monkeypatch.setattr(
        demo,
        "check_password_breach",
        lambda password: {
            "status": "unavailable",
            "compromised": None,
            "count": None,
        },
    )

    response = demo.app.test_client().post(
        "/register",
        json={"username": "frank", "password": "Demo-Password"},
    )

    assert response.status_code == 503
    assert "frank" not in demo.USERS


def test_register_accepts_password_not_found_in_breaches(monkeypatch):
    demo.BREACH_CHECK_ENABLED = True
    monkeypatch.setattr(
        demo,
        "check_password_breach",
        lambda password: {
            "status": "not_found",
            "compromised": False,
            "count": 0,
        },
    )

    response = demo.app.test_client().post(
        "/register",
        json={"username": "grace", "password": "Synthetic-Password"},
    )

    assert response.status_code == 201
    assert "grace" in demo.USERS
