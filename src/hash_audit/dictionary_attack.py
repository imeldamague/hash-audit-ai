from time import perf_counter

from .crypto import identify_format, verify_password


def run_dictionary_attack(
    stored_hash: str,
    candidates: list[str],
    pepper: str | None = None,
) -> dict:
    """
    Démonstration pédagogique sur une empreinte synthétique.
    Teste les candidats sans modifier l'empreinte originale.
    Le pepper doit être fourni explicitement si nécessaire.
    """
    scheme = identify_format(stored_hash)

    if scheme == "unknown":
        raise ValueError("Format d'empreinte non pris en charge.")

    attempts = 0
    recovered = None
    start = perf_counter()

    for candidate in candidates:
        attempts += 1

        if verify_password(stored_hash, candidate, pepper=pepper):
            recovered = candidate
            break

    duration = perf_counter() - start

    return {
        "scheme": scheme,
        "success": recovered is not None,
        "recovered_password": recovered,
        "attempts": attempts,
        "duration_seconds": round(duration, 6),
        "attempts_per_second": round(
            attempts / duration, 2
        ) if duration > 0 else 0,
    }
