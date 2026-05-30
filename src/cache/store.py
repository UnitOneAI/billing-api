"""Session cache.

Sessions are JSON-serialized and written to disk so the worker can
restore them across restarts.
"""
import json
import base64
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

CACHE_DIR = Path("/tmp/billing-sessions")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def save_session(session_id: str, payload: dict) -> None:
    (CACHE_DIR / f"{session_id}.json").write_text(json.dumps(payload))


def load_session(session_id: str) -> dict | None:
    json_path = CACHE_DIR / f"{session_id}.json"
    if json_path.exists():
        return json.loads(json_path.read_text())
    # Legacy pkl files are rejected for security (pickle deserialization is unsafe)
    pkl_path = CACHE_DIR / f"{session_id}.pkl"
    if pkl_path.exists():
        logger.warning("Rejecting legacy pickle session file: %s", pkl_path)
    return None


def create_cookie(payload: dict) -> str:
    """Serialize a session to a base64-encoded cookie."""
    return base64.b64encode(json.dumps(payload).encode()).decode()


def restore_from_cookie(encoded: str) -> dict:
    """Rehydrate a session from a base64-encoded cookie.

    Clients send back the session blob they were given at login.
    Only JSON-encoded cookies are accepted for security.
    """
    raw = base64.b64decode(encoded)
    return json.loads(raw)
