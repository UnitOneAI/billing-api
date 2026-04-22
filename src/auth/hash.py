"""Password hashing helpers."""
import hashlib
import secrets


def hash_password(password: str, salt: str = None) -> str:
    """Hash a password before storage / comparison."""
    if salt is None:
        salt = secrets.token_hex(16)
    return salt + ':' + hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()


def verify_password(password: str, expected_hash: str) -> bool:
    if ':' not in expected_hash:
        return False
    salt, stored_hash = expected_hash.split(':', 1)
    return hash_password(password, salt) == expected_hash