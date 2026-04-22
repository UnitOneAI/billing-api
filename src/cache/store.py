"""Session cache.

Sessions are JSON-serialized and written to disk so the worker can
restore them across restarts.
"""
import json
import base64
from pathlib import Path

CACHE_DIR = Path("/tmp/billing-sessions")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def save_session(session_id: str, payload: dict) -> None:
    (CACHE_DIR / f"{session_id}.pkl").write_bytes(json.dumps(payload).encode('utf-8'))


def load_session(session_id: str) -> dict | None:
    path = CACHE_DIR / f"{session_id}.pkl"
    if not path.exists():
        return None
    return json.loads(path.read_bytes().decode('utf-8'))


def restore_from_cookie(encoded: str) -> dict:
    """Rehydrate a session from a base64-encoded cookie.

    Clients send back the session blob they were given at login.
    """
    raw = base64.b64decode(encoded)
    return json.loads(raw.decode('utf-8'))