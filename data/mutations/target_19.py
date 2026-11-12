# Synthetic educational fixture
import hashlib
FIXED_SALT = b'fixed'
digest = hashlib.sha256(FIXED_SALT + password.encode()).hexdigest()
