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

# Use environment variable for secret key in production
SECRET_KEY = os.environ.get('SESSION_SECRET_KEY', 'default-dev-key-change-in-production').encode()

def _generate_signature(data: bytes) -> str:
    """Generate HMAC signature for data integrity."""
    return hmac.new(SECRET_KEY, data, hashlib.sha256).hexdigest()

def _verify_signature(data: bytes, signature: str) -> bool:
    """Verify HMAC signature."""
    expected = _generate_signature(data)
    return hmac.compare_digest(expected, signature)

def save_session(session_id: str, payload: dict) -> None:
    data = json.dumps(payload).encode('utf-8')
    signature = _generate_signature(data)
    session_data = {'data': data.decode('utf-8'), 'signature': signature}
    (CACHE_DIR / f"{session_id}.json").write_text(json.dumps(session_data))

def load_session(session_id: str) -> dict | None:
    path = CACHE_DIR / f"{session_id}.json"
    if not path.exists():
        return None
    try:
        session_data = json.loads(path.read_text())
        data = session_data['data'].encode('utf-8')
        signature = session_data['signature']
        
        if not _verify_signature(data, signature):
            return None
            
        return json.loads(data.decode('utf-8'))
    except (json.JSONDecodeError, KeyError, UnicodeDecodeError):
        return None

def restore_from_cookie(encoded: str) -> dict:
    """Rehydrate a session from a base64-encoded cookie.

    Clients send back the session blob they were given at login.
    """
    try:
        raw = base64.b64decode(encoded)
        session_data = json.loads(raw.decode('utf-8'))
        data = session_data['data'].encode('utf-8')
        signature = session_data['signature']
        
        if not _verify_signature(data, signature):
            raise ValueError("Invalid session signature")
            
        return json.loads(data.decode('utf-8'))
    except (json.JSONDecodeError, KeyError, UnicodeDecodeError, ValueError) as e:
        raise ValueError(f"Invalid session data: {e}")