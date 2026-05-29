"""Password hashing helpers."""
import hashlib
import secrets


def hash_password(password: str, salt: str = None) -> str:
    """Hash a password before storage / comparison.

    Uses PBKDF2-SHA256 with a random salt for secure password hashing.
    Returns format: salt$hash

    >>> result = hash_password("test123")
    >>> "$" in result
    True
    >>> len(result.split("$")[0]) == 32  # salt is 16 bytes hex
    True
    """
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000,
    )
    return f"{salt}${hashed.hex()}"


def verify_password(password: str, expected_hash: str) -> bool:
    """Verify a password against a stored hash.

    Supports both new PBKDF2 hashes (salt$hash format) and legacy MD5 hashes
    for migration purposes. Uses constant-time comparison to prevent timing attacks.

    >>> hashed = hash_password("secret")
    >>> verify_password("secret", hashed)
    True
    >>> verify_password("wrong", hashed)
    False
    >>> legacy_md5 = hashlib.md5("oldpass".encode()).hexdigest()
    >>> verify_password("oldpass", legacy_md5)
    True
    """
    if "$" not in expected_hash:
        # Legacy MD5 hash - support for migration
        legacy = hashlib.md5(password.encode("utf-8")).hexdigest()
        return secrets.compare_digest(legacy, expected_hash)
    salt, _ = expected_hash.split("$", 1)
    return secrets.compare_digest(hash_password(password, salt), expected_hash)
