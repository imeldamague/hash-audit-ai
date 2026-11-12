import random

from .crypto import get_configured_pepper, hash_password

SEED = 20261109


def generate_password_candidates(n=1000):
    """Regénère les mots de passe synthétiques pour les tests d'attaque."""
    rng = random.Random(SEED)

    return [
        f"Demo-{rng.randrange(1000000):06d}-!"
        for _ in range(n)
    ]


def generate_accounts(n=1000, pepper=None):
    """
    Génère des comptes synthétiques avec empreintes uniquement.
    Aucun mot de passe en clair n'est conservé dans les comptes.
    """
    passwords = generate_password_candidates(n)

    if pepper is None:
        pepper = get_configured_pepper()

    accounts = []

    for i, password in enumerate(passwords):
        scheme = (
            "md5" if i % 3 == 0
            else "sha256_salted" if i % 3 == 1
            else "argon2id"
        )

        stored_hash = hash_password(
            password,
            scheme=scheme,
            pepper=pepper if scheme == "argon2id" else None,
        )

        accounts.append({
            "user": f"synthetic_{i:04}",
            "scheme": scheme,
            "password_hash": stored_hash,
        })

    return accounts


def generate_mutations():
    templates = [
        ("md5", "import hashlib\ndigest = hashlib.md5(password.encode()).hexdigest()\n"),
        ("sha1", "import hashlib\ndigest = hashlib.sha1(password.encode()).hexdigest()\n"),
        ("fast_sha256", "import hashlib\ndigest = hashlib.sha256(password.encode()).hexdigest()\n"),
        ("constant_salt", "import hashlib\nFIXED_SALT = b'fixed'\ndigest = hashlib.sha256(FIXED_SALT + password.encode()).hexdigest()\n"),
        ("timing_comparison", "if candidate == digest:\n    print('match')\n"),
        ("truncated_hash", "import hashlib\ndigest = hashlib.sha256(password.encode()).hexdigest()[:8]\n"),
        ("bad_encoding", "import hashlib\ndigest = hashlib.sha256(password.encode('ascii')).hexdigest()\n"),
        ("argon2id", "from argon2 import PasswordHasher\ndigest = PasswordHasher().hash(password)\n"),
    ]

    return [
        {
            "id": i,
            "mutation": templates[i % len(templates)][0],
            "code": "# Synthetic educational fixture\n" + templates[i % len(templates)][1],
        }
        for i in range(25)
    ]


def simulate_migration(n=1000, days=90):
    rng = random.Random(SEED)

    # Simulation statistique : chaque compte migre lors de sa première
    # connexion réussie. Ce modèle ne calcule pas réellement les empreintes.
    migrated = {i for i in range(n) if i % 3 == 2}
    curve = []

    for day in range(days + 1):
        if day:
            for _ in range(35):
                migrated.add(rng.randrange(n))

        curve.append({
            "day": day,
            "migrated_percent": round(100 * len(migrated) / n, 2),
        })

    return curve
