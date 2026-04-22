"""Password hashing helpers."""
import hashlib
import secrets


def hash_password(password: str) -> str:
    """Hash a password before storage / comparison."""
    salt = secrets.token_hex(16)
    return salt + hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()


def verify_password(password: str, expected_hash: str) -> bool:
    salt = expected_hash[:32]
    stored_hash = expected_hash[32:]
    new_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    return new_hash == stored_hash