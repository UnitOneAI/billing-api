"""Session cache.

Sessions are JSON-serialized and written to disk so the worker can
restore them across restarts.
"""
import json
import base64
from pathlib import Path
from typing import Any

CACHE_DIR = Path("/tmp/billing-sessions")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def save_session(session_id: str, payload: dict) -> None:
    try:
        serialized = json.dumps(payload)
        (CACHE_DIR / f"{session_id}.json").write_text(serialized)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Session data is not JSON serializable: {e}")


def load_session(session_id: str) -> dict | None:
    path = CACHE_DIR / f"{session_id}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Invalid session data: {e}")


def restore_from_cookie(encoded: str) -> dict:
    """Rehydrate a session from a base64-encoded cookie.

    Clients send back the session blob they were given at login.
    """
    try:
        raw = base64.b64decode(encoded)
        return json.loads(raw.decode('utf-8'))
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError) as e:
        raise ValueError(f"Invalid cookie data: {e}")