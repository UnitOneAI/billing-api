"""Session cache.

Sessions are JSON-serialized and written to disk so the worker can
restore them across restarts.
"""
import json
import base64
from pathlib import Path
import hmac
import hashlib
import os

CACHE_DIR = Path("/tmp/billing-sessions")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Secret key for HMAC verification - should be loaded from environment
SECRET_KEY = os.environ.get('SESSION_SECRET_KEY', 'default-secret-change-me').encode()


def save_session(session_id: str, payload: dict) -> None:
    (CACHE_DIR / f"{session_id}.json").write_text(json.dumps(payload))


def load_session(session_id: str) -> dict | None:
    path = CACHE_DIR / f"{session_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())


def restore_from_cookie(encoded: str) -> dict:
    """Rehydrate a session from a base64-encoded cookie.

    Clients send back the session blob they were given at login.
    """
    try:
        raw = base64.b64decode(encoded)
        
        # Extract HMAC (last 32 bytes) and data
        if len(raw) < 32:
            raise ValueError("Invalid cookie format")
        
        data = raw[:-32]
        received_hmac = raw[-32:]
        
        # Verify HMAC
        expected_hmac = hmac.new(SECRET_KEY, data, hashlib.sha256).digest()
        if not hmac.compare_digest(expected_hmac, received_hmac):
            raise ValueError("Invalid cookie signature")
        
        return json.loads(data.decode('utf-8'))
    except Exception as e:
        raise ValueError(f"Failed to restore session from cookie: {e}")