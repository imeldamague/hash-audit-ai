import hashlib
import hmac
import os
import re
import secrets
import urllib.error
import urllib.request

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

ARGON = PasswordHasher(
    time_cost=2,
    memory_cost=19456,
    parallelism=1
)


def get_configured_pepper() -> str | None:
    """Charge le pepper depuis la variable d'environnement."""
    return os.environ.get("HASH_AUDIT_PEPPER") or None


def _prepare_password(password: str, pepper: str | None = None) -> str:
    """Combine le mot de passe et le pepper avant Argon2id."""
    if pepper is None:
        return password

    if not pepper:
        raise ValueError("Le pepper ne peut pas être vide.")

    return hmac.new(
        pepper.encode("utf-8"),
        password.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def identify_format(stored: str) -> str:
    if stored.startswith("$argon2id$"):
        return "argon2id"
    if stored.startswith(("$2a$", "$2b$", "$2y$")):
        return "bcrypt"
    if stored.startswith("scrypt$"):
        return "scrypt"
    if stored.startswith("pbkdf2$"):
        return "pbkdf2"
    if re.fullmatch(r"[a-fA-F0-9]{32}", stored):
        return "md5"
    if re.fullmatch(r"[a-fA-F0-9]{40}", stored):
        return "sha1"
    if re.fullmatch(r"[a-fA-F0-9]{64}", stored):
        return "sha256_unsalted"
    if re.fullmatch(r"sha256\$[a-fA-F0-9]+\$[a-fA-F0-9]{64}", stored):
        return "sha256_salted"
    return "unknown"


def hash_password(
    password: str,
    scheme: str = "argon2id",
    pepper: str | None = None
) -> str:
    raw = password.encode("utf-8")

    if scheme == "argon2id":
        prepared = _prepare_password(password, pepper)
        return ARGON.hash(prepared)

    if pepper is not None:
        raise ValueError("Le pepper est pris en charge uniquement avec Argon2id.")

    if scheme == "md5":
        return hashlib.md5(raw).hexdigest()  # Educational target only

    if scheme == "sha256_salted":
        salt = secrets.token_hex(16)
        digest = hashlib.sha256(bytes.fromhex(salt) + raw).hexdigest()
        return f"sha256${salt}${digest}"

    raise ValueError("Unsupported scheme")


def verify_password(
    stored: str,
    password: str,
    pepper: str | None = None
) -> bool:
    scheme = identify_format(stored)

    if scheme == "argon2id":
        try:
            prepared = _prepare_password(password, pepper)
            return bool(ARGON.verify(stored, prepared))
        except (VerifyMismatchError, VerificationError, ValueError):
            return False

    if pepper is not None:
        return False

    if scheme == "md5":
        candidate = hashlib.md5(password.encode()).hexdigest()
        return hmac.compare_digest(stored, candidate)

    if scheme == "sha256_salted":
        try:
            _, salt, digest = stored.split("$")
            candidate = hashlib.sha256(
                bytes.fromhex(salt) + password.encode()
            ).hexdigest()
            return hmac.compare_digest(digest, candidate)
        except (ValueError, TypeError):
            return False

    return False


def migrate_on_login(
    stored: str,
    password: str,
    pepper: str | None = None
) -> tuple[bool, str]:
    scheme = identify_format(stored)

    if scheme == "argon2id":
        # V?rifie d'abord avec le pepper fourni.
        if pepper is not None:
            if verify_password(stored, password, pepper=pepper):
                return True, stored

            # Permet de migrer une ancienne empreinte Argon2id
            # qui avait ?t? cr??e sans pepper.
            if verify_password(stored, password):
                return True, hash_password(password, "argon2id", pepper)

            return False, stored

        # Sans pepper, seules les empreintes sans pepper sont valides.
        if verify_password(stored, password):
            return True, stored

        return False, stored

    # Les anciens formats sont v?rifi?s sans pepper,
    # puis migr?s vers Argon2id.
    if not verify_password(stored, password):
        return False, stored

    return True, hash_password(password, "argon2id", pepper)


def local_breach_check(password: str, sha1_hashes: set[str]) -> bool:
    # Local synthetic hash set; no network request.
    digest = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = digest[:5], digest[5:]
    candidates = {
        h[5:] for h in sha1_hashes
        if h.startswith(prefix)
    }
    return suffix in candidates


def check_password_breach(password: str, timeout: float = 5.0) -> dict:
    """
    V?rifie un mot de passe avec l'API Pwned Passwords (k-anonymat).

    Seuls les cinq premiers caract?res du SHA-1 sont transmis.
    La comparaison du suffixe est effectu?e localement.

    Le statut vaut compromised, not_found ou unavailable.
    """
    if not isinstance(password, str) or not password:
        raise ValueError("Le mot de passe doit ?tre une cha?ne non vide.")

    if timeout <= 0:
        raise ValueError("Le d?lai d'attente doit ?tre positif.")

    digest = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = digest[:5], digest[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Hash-Audit-AI/1.0",
            "Add-Padding": "true",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("ascii")

        for line in body.splitlines():
            parts = line.strip().split(":")
            if len(parts) != 2:
                continue

            returned_suffix, count_text = parts

            if returned_suffix.upper() == suffix:
                return {
                    "status": "compromised",
                    "compromised": True,
                    "count": int(count_text),
                }

        return {
            "status": "not_found",
            "compromised": False,
            "count": 0,
        }

    except (urllib.error.URLError, TimeoutError, OSError, UnicodeError):
        return {
            "status": "unavailable",
            "compromised": None,
            "count": None,
        }
