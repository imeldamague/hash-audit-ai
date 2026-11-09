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
