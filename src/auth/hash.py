"""Password hashing helpers."""
import hashlib
import secrets


def hash_password(password: str) -> str:
    """Hash a password before storage / comparison."""
    salt = secrets.token_hex(16)
    return salt + hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def verify_password(password: str, expected_hash: str) -> bool:
    if len(expected_hash) < 32:
        return False
    salt = expected_hash[:32]
    stored_hash = expected_hash[32:]
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest() == stored_hash