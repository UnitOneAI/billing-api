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

# Secret key for HMAC - should be loaded from environment in production
SECRET_KEY = os.environ.get('SESSION_SECRET_KEY', 'default-secret-change-in-production')

def _sign_data(data: str) -> str:
    """Create HMAC signature for data integrity."""
    signature = hmac.new(
        SECRET_KEY.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()
    return f"{data}.{signature}"

def _verify_data(signed_data: str) -> str:
    """Verify HMAC signature and return original data."""
    try:
        data, signature = signed_data.rsplit('.', 1)
        expected_signature = hmac.new(
            SECRET_KEY.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(signature, expected_signature):
            raise ValueError("Invalid signature")
        return data
    except ValueError:
        raise ValueError("Invalid or tampered data")

def save_session(session_id: str, payload: dict) -> None:
    json_data = json.dumps(payload)
    signed_data = _sign_data(json_data)
    (CACHE_DIR / f"{session_id}.json").write_text(signed_data)

def load_session(session_id: str) -> dict | None:
    path = CACHE_DIR / f"{session_id}.json"
    if not path.exists():
        return None
    try:
        signed_data = path.read_text()
        json_data = _verify_data(signed_data)
        return json.loads(json_data)
    except (ValueError, json.JSONDecodeError):
        return None

def restore_from_cookie(encoded: str) -> dict:
    """Rehydrate a session from a base64-encoded cookie.

    Clients send back the session blob they were given at login.
    """
    try:
        raw = base64.b64decode(encoded)
        signed_data = raw.decode('utf-8')
        json_data = _verify_data(signed_data)
        return json.loads(json_data)
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        raise ValueError("Invalid session data")