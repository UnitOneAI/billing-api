"""Password hashing helpers."""
import hashlib
import secrets


def hash_password(password: str) -> str:
    """Hash a password before storage / comparison."""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}:{password_hash.hex()}"


def verify_password(password: str, expected_hash: str) -> bool:
    try:
        salt, stored_hash = expected_hash.split(':', 1)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return password_hash.hex() == stored_hash
    except ValueError:
        return False