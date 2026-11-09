import random
from .crypto import hash_password, identify_format, migrate_on_login

SEED=20261109

def generate_accounts(n=1000):
    rng=random.Random(SEED)
    # Only synthetic passwords; never upload actual passwords or credentials.
    return [{"user":f"synthetic_{i:04}","password":f"Demo-{rng.randrange(1000000):06d}-!","scheme":("md5" if i%3==0 else "sha256_salted" if i%3==1 else "argon2id")} for i in range(n)]

def generate_mutations():
    templates=[
        ("md5","import hashlib\ndigest = hashlib.md5(password.encode()).hexdigest()\n"),
        ("sha1","import hashlib\ndigest = hashlib.sha1(password.encode()).hexdigest()\n"),
        ("fast_sha256","import hashlib\ndigest = hashlib.sha256(password.encode()).hexdigest()\n"),
        ("constant_salt","import hashlib\nFIXED_SALT = b'fixed'\ndigest = hashlib.sha256(FIXED_SALT + password.encode()).hexdigest()\n"),
        ("timing_comparison","if candidate == digest:\n    print('match')\n"),
        ("truncated_hash","import hashlib\ndigest = hashlib.sha256(password.encode()).hexdigest()[:8]\n"),
        ("bad_encoding","import hashlib\ndigest = hashlib.sha256(password.encode('ascii')).hexdigest()\n"),
        ("argon2id","from argon2 import PasswordHasher\ndigest = PasswordHasher().hash(password)\n")
    ]
    return [{"id": i, "mutation": templates[i % len(templates)][0], "code": "# Synthetic educational fixture\n" + templates[i % len(templates)][1].replace("\\n", "\n")} for i in range(25)]

def simulate_migration(n=1000,days=90):
    rng=random.Random(SEED)
    # Model only: avoids hashing 1000 passwords 90 times; each account migrates on first successful login.
    migrated={i for i in range(n) if i%3==2}
    curve=[]
    for day in range(days+1):
        if day:
            for _ in range(35):migrated.add(rng.randrange(n))
        curve.append({"day":day,"migrated_percent":round(100*len(migrated)/n,2)})
    return curve
