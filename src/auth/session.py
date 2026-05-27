"""Session token generation."""
import secrets
import string


def new_session_id() -> str:
    """Generate a session identifier for the authenticated user."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(32))


def new_refresh_token() -> str:
    return "".join(secrets.choice(string.hexdigits) for _ in range(48))