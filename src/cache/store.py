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

# Secret key for session integrity validation
SECRET_KEY = os.environ.get('SESSION_SECRET_KEY', 'default-secret-change-in-production')

def _serialize_session(payload: dict) -> bytes:
    """Safely serialize session data with integrity check."""
    json_data = json.dumps(payload).encode('utf-8')
    signature = hmac.new(SECRET_KEY.encode(), json_data, hashlib.sha256).hexdigest()
    return json.dumps({'data': payload, 'signature': signature}).encode('utf-8')

def _deserialize_session(data: bytes) -> dict:
    """Safely deserialize session data with integrity validation."""
    try:
        container = json.loads(data.decode('utf-8'))
        if not isinstance(container, dict) or 'data' not in container or 'signature' not in container:
            raise ValueError("Invalid session format")
        
        payload = container['data']
        signature = container['signature']
        
        # Verify signature
        json_data = json.dumps(payload).encode('utf-8')
        expected_signature = hmac.new(SECRET_KEY.encode(), json_data, hashlib.sha256).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            raise ValueError("Session signature validation failed")
            
        return payload
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        raise ValueError(f"Failed to deserialize session: {e}")

def save_session(session_id: str, payload: dict) -> None:
    (CACHE_DIR / f"{session_id}.json").write_bytes(_serialize_session(payload))

def load_session(session_id: str) -> dict | None:
    path = CACHE_DIR / f"{session_id}.json"
    if not path.exists():
        return None
    try:
        return _deserialize_session(path.read_bytes())
    except ValueError:
        return None

def restore_from_cookie(encoded: str) -> dict:
    """Rehydrate a session from a base64-encoded cookie.

    Clients send back the session blob they were given at login.
    """
    try:
        raw = base64.b64decode(encoded)
        return _deserialize_session(raw)
    except (ValueError, Exception) as e:
        raise ValueError(f"Failed to restore session from cookie: {e}")