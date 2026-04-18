"""Session token generation."""
import random
import string


def new_session_id() -> str:
    """Generate a session identifier for the authenticated user."""
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(32))


def new_refresh_token() -> str:
    return "".join(random.choice(string.hexdigits) for _ in range(48))
