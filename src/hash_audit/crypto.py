import hashlib
import hmac
import re
import secrets
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

ARGON = PasswordHasher(time_cost=2, memory_cost=19456, parallelism=1)

def identify_format(stored: str) -> str:
    if stored.startswith("$argon2id$"): return "argon2id"
    if stored.startswith(("$2a$", "$2b$", "$2y$")): return "bcrypt"
    if stored.startswith("scrypt$"): return "scrypt"
    if stored.startswith("pbkdf2$"): return "pbkdf2"
    if re.fullmatch(r"[a-fA-F0-9]{32}", stored): return "md5"
    if re.fullmatch(r"[a-fA-F0-9]{40}", stored): return "sha1"
    if re.fullmatch(r"[a-fA-F0-9]{64}", stored): return "sha256_unsalted"
    if re.fullmatch(r"sha256\$[a-fA-F0-9]+\$[a-fA-F0-9]{64}", stored): return "sha256_salted"
    return "unknown"

def hash_password(password: str, scheme: str = "argon2id") -> str:
    raw = password.encode("utf-8")
    if scheme == "argon2id": return ARGON.hash(password)
    if scheme == "md5": return hashlib.md5(raw).hexdigest()  # VULNERABLE: educational target only
    if scheme == "sha256_salted":
        salt=secrets.token_hex(16)
        return f"sha256${salt}${hashlib.sha256(bytes.fromhex(salt)+raw).hexdigest()}"  # deliberately fast
    raise ValueError("Unsupported scheme")

def verify_password(stored: str, password: str) -> bool:
    scheme=identify_format(stored)
    if scheme == "argon2id":
        try: return bool(ARGON.verify(stored,password))
        except (VerifyMismatchError,VerificationError,ValueError): return False
    if scheme == "md5": return hmac.compare_digest(stored,hashlib.md5(password.encode()).hexdigest())
    if scheme == "sha256_salted":
        _,salt,digest=stored.split("$")
        candidate=hashlib.sha256(bytes.fromhex(salt)+password.encode()).hexdigest()
        return hmac.compare_digest(digest,candidate)
    return False

def migrate_on_login(stored: str,password: str) -> tuple[bool,str]:
    if not verify_password(stored,password): return False,stored
    if identify_format(stored)=="argon2id": return True,stored
    return True,hash_password(password,"argon2id")

def local_breach_check(password: str, sha1_hashes: set[str]) -> bool:
    # Entirely local, synthetic hash set; no network request or real password corpus.
    digest=hashlib.sha1(password.encode()).hexdigest().upper()
    prefix,suffix=digest[:5],digest[5:]
    candidates={h[5:] for h in sha1_hashes if h.startswith(prefix)}
    return suffix in candidates
