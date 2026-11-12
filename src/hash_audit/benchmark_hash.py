import csv
from pathlib import Path

import bcrypt
import hashlib
import secrets
from statistics import mean
from time import perf_counter

from argon2 import PasswordHasher

PASSWORD = "Demo-Benchmark-2026!"
SALT = b"hash-audit-ai-salt"
REPETITIONS = 10

ARGON = PasswordHasher(
    time_cost=2,
    memory_cost=19456,
    parallelism=1
)


def benchmark_argon2(password):
    encoded = ARGON.hash(password)
    return encoded, lambda candidate: ARGON.verify(encoded, candidate)


def benchmark_scrypt(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(
        password.encode(),
        salt=salt,
        n=2**14,
        r=8,
        p=1,
        dklen=32
    )

    def verify(candidate):
        result = hashlib.scrypt(
            candidate.encode(),
            salt=salt,
            n=2**14,
            r=8,
            p=1,
            dklen=32
        )
        return secrets.compare_digest(digest, result)

    return (salt, digest), verify


def benchmark_bcrypt(password):
    salt = bcrypt.gensalt(rounds=12)
    encoded = bcrypt.hashpw(password.encode(), salt)

    def verify(candidate):
        return bcrypt.checkpw(candidate.encode(), encoded)

    return encoded, verify


def benchmark_pbkdf2(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        600000
    )

    def verify(candidate):
        result = hashlib.pbkdf2_hmac(
            "sha256",
            candidate.encode(),
            salt,
            600000
        )
        return secrets.compare_digest(digest, result)

    return (salt, digest), verify


ALGORITHMS = {
    "Argon2id": benchmark_argon2,
    "scrypt": benchmark_scrypt,
    "bcrypt": benchmark_bcrypt,
    "PBKDF2-SHA256": benchmark_pbkdf2,
}


def run_benchmark():
    results = []

    for name, function in ALGORITHMS.items():
        hash_times = []
        verify_times = []

        for _ in range(REPETITIONS):
            start = perf_counter()
            encoded, verify = function(PASSWORD)
            hash_times.append(perf_counter() - start)

            start = perf_counter()
            valid = verify(PASSWORD)
            verify_times.append(perf_counter() - start)

            if not valid:
                raise RuntimeError(f"Échec de vérification : {name}")

        results.append({
            "algorithm": name,
            "hash_ms": round(mean(hash_times) * 1000, 2),
            "verify_ms": round(mean(verify_times) * 1000, 2),
            "repetitions": REPETITIONS,
            "verification": "success",
        })

    return results


if __name__ == "__main__":
    results = run_benchmark()

    output = Path("results")
    output.mkdir(exist_ok=True)

    csv_path = output / "hash_benchmark.csv"

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    for result in results:
        print(result)

    print(f"\nR?sultats enregistr?s dans : {csv_path}")
