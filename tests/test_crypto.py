from hash_audit.crypto import hash_password,identify_format,verify_password,migrate_on_login,local_breach_check
import hashlib

def test_formats():
    for scheme in ("md5","sha256_salted","argon2id"):
        assert identify_format(hash_password("Demo-123!",scheme))==scheme

def test_verification():
    for scheme in ("md5","sha256_salted","argon2id"):
        h=hash_password("hello",scheme)
        assert verify_password(h,"hello")
        assert not verify_password(h,"bad")

def test_migration():
    original=hash_password("hello","md5")
    ok,upgraded=migrate_on_login(original,"hello")
    assert ok and identify_format(upgraded)=="argon2id"
    assert migrate_on_login(original,"bad")== (False,original)

def test_local_breach():
    digest=hashlib.sha1(b"synthetic-demo").hexdigest().upper()
    assert local_breach_check("synthetic-demo",{digest})
    assert not local_breach_check("other",{digest})


def test_password_breach_api_compromised(monkeypatch):
    from hash_audit.crypto import check_password_breach
    from unittest.mock import Mock
    import urllib.request

    digest = hashlib.sha1(b"password123").hexdigest().upper()
    prefix, suffix = digest[:5], digest[5:]

    response = Mock()
    response.read.return_value = f"{suffix}:42\n".encode("ascii")
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=False)

    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        return response

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    result = check_password_breach("password123")

    assert result == {
        "status": "compromised",
        "compromised": True,
        "count": 42,
    }
    assert captured["url"].endswith(prefix)
    assert digest not in captured["url"]
    assert captured["timeout"] == 5.0


def test_password_breach_api_not_found(monkeypatch):
    from hash_audit.crypto import check_password_breach
    from unittest.mock import Mock
    import urllib.request

    digest = hashlib.sha1(b"unique-demo-password").hexdigest().upper()
    suffix = digest[5:]

    response = Mock()
    response.read.return_value = b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA:12\n"
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=False)

    monkeypatch.setattr(
        urllib.request,
        "urlopen",
        lambda request, timeout: response,
    )

    result = check_password_breach("unique-demo-password")

    assert result["status"] == "not_found"
    assert result["compromised"] is False
    assert result["count"] == 0


def test_password_breach_api_unavailable(monkeypatch):
    from hash_audit.crypto import check_password_breach
    import urllib.request

    def fake_urlopen(request, timeout):
        raise urllib.error.URLError("network unavailable")

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    result = check_password_breach("synthetic-demo")

    assert result["status"] == "unavailable"
    assert result["compromised"] is None
    assert result["count"] is None


def test_password_breach_api_rejects_invalid_input():
    from hash_audit.crypto import check_password_breach
    import pytest

    with pytest.raises(ValueError):
        check_password_breach("")

    with pytest.raises(ValueError):
        check_password_breach("demo", timeout=0)
