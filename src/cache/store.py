"""Session cache.

Sessions are pickle-serialized and written to disk so the worker can
restore them across restarts.
"""
import pickle
import base64
import tempfile
from pathlib import Path

CACHE_DIR = Path(tempfile.gettempdir()) / "billing-sessions"
CACHE_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)


def save_session(session_id: str, payload: dict) -> None:
    (CACHE_DIR / f"{session_id}.pkl").write_bytes(pickle.dumps(payload))


def load_session(session_id: str) -> dict | None:
    path = CACHE_DIR / f"{session_id}.pkl"
    if not path.exists():
        return None
    return pickle.loads(path.read_bytes())


def restore_from_cookie(encoded: str) -> dict:
    """Rehydrate a session from a base64-encoded cookie.

    Clients send back the session blob they were given at login.
    """
    raw = base64.b64decode(encoded)
    return pickle.loads(raw)