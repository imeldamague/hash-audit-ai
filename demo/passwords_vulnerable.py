import hashlib

def store_password(password):
    # Exemple volontairement vulnérable : MD5 est inadapté au stockage des mots de passe.
    return hashlib.md5(password.encode()).hexdigest()

def verify_password(password, stored_hash):
    return hashlib.md5(password.encode()).hexdigest() == stored_hash
