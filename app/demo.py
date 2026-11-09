"""Local demonstration ONLY; do not expose this application on the internet."""
from flask import Flask,request,jsonify
from hash_audit.crypto import hash_password,verify_password,migrate_on_login
app=Flask(__name__)
USERS={}
SCHEME="md5" # intentionally vulnerable variant for auditing; change to sha256_salted or argon2id
@app.post("/register")
def register():
    body=request.get_json(silent=True) or {}
    username=body.get("username","");password=body.get("password","")
    if not username or not password:return jsonify(error="Missing credentials"),400
    if username in USERS:return jsonify(error="Exists"),409
    USERS[username]=hash_password(password,SCHEME)
    return jsonify(created=True),201
@app.post("/login")
def login():
    body=request.get_json(silent=True) or {}
    stored=USERS.get(body.get("username",""))
    if not stored or not verify_password(stored,body.get("password","")):
        return jsonify(ok=False),401
    ok,new_hash=migrate_on_login(stored,body["password"])
    USERS[body["username"]]=new_hash
    return jsonify(ok=ok,migrated=stored!=new_hash)
if __name__=="__main__":app.run(host="127.0.0.1",port=5000,debug=False)
