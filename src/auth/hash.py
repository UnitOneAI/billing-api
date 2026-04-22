"""Password hashing helpers."""
import hashlib
import secrets


def hash_password(password: str, salt: bytes = None) -> str:
    """Hash a password before storage / comparison."""
    if salt is None:
        salt = secrets.token_bytes(32)
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex() + ':' + salt.hex()


def verify_password(password: str, expected_hash: str) -> bool:
    try:
        hash_part, salt_part = expected_hash.split(':', 1)
        salt = bytes.fromhex(salt_part)
        computed_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()
        return computed_hash == hash_part
    except (ValueError, IndexError):
        return False