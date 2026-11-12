"""Local demonstration ONLY; do not expose this application on the internet."""

from flask import Flask, request, jsonify

from hash_audit.crypto import (
    get_configured_pepper,
    hash_password,
    identify_format,
    verify_password,
    migrate_on_login,
    check_password_breach,
)

app = Flask(__name__)

USERS = {}

# MD5 is intentionally used to demonstrate migration.
# Other supported demonstration schemes: sha256_salted, argon2id.
SCHEME = "md5"

# Enable the external k-anonymity check for registration.
BREACH_CHECK_ENABLED = False

# Load the pepper from the environment at application startup.
PEPPER = get_configured_pepper()


@app.post("/register")
def register():
    body = request.get_json(silent=True) or {}
    username = body.get("username", "")
    password = body.get("password", "")

    if not username or not password:
        return jsonify(error="Missing credentials"), 400

    if BREACH_CHECK_ENABLED:
        breach = check_password_breach(password)

        if breach["status"] == "unavailable":
            return jsonify(
                error="Password breach verification unavailable"
            ), 503

        if breach["compromised"]:
            return jsonify(
                error="Password found in known breaches",
                occurrences=breach["count"],
            ), 400

    if username in USERS:
        return jsonify(error="Exists"), 409

    USERS[username] = hash_password(
        password,
        SCHEME,
        pepper=PEPPER if SCHEME == "argon2id" else None,
    )

    return jsonify(created=True), 201


@app.post("/login")
def login():
    body = request.get_json(silent=True) or {}
    username = body.get("username", "")
    password = body.get("password", "")

    stored = USERS.get(username)

    if not stored:
        return jsonify(ok=False), 401

    # Legacy hashes are verified without pepper.
    # Argon2id hashes use the configured pepper.
    scheme = identify_format(stored)
    verification_pepper = PEPPER if scheme == "argon2id" else None

    if not verify_password(
        stored,
        password,
        pepper=verification_pepper,
    ):
        return jsonify(ok=False), 401

    ok, new_hash = migrate_on_login(
        stored,
        password,
        pepper=PEPPER,
    )

    if not ok:
        return jsonify(ok=False), 401

    USERS[username] = new_hash

    return jsonify(
        ok=True,
        migrated=stored != new_hash,
        scheme=identify_format(new_hash),
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
