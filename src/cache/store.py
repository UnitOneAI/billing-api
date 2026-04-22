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

# Secret key for HMAC validation - should be loaded from environment
SECRET_KEY = os.environ.get('SESSION_SECRET_KEY', 'default-key-change-in-production')

def _generate_signature(data: bytes) -> str:
    """Generate HMAC signature for data integrity."""
    return hmac.new(SECRET_KEY.encode(), data, hashlib.sha256).hexdigest()

def _verify_signature(data: bytes, signature: str) -> bool:
    """Verify HMAC signature."""
    expected = _generate_signature(data)
    return hmac.compare_digest(expected, signature)

def save_session(session_id: str, payload: dict) -> None:
    data = json.dumps(payload).encode('utf-8')
    signature = _generate_signature(data)
    with open(CACHE_DIR / f"{session_id}.json", 'w') as f:
        json.dump({'data': payload, 'signature': signature}, f)

def load_session(session_id: str) -> dict | None:
    path = CACHE_DIR / f"{session_id}.json"
    if not path.exists():
        return None
    
    try:
        with open(path, 'r') as f:
            container = json.load(f)
        
        data = json.dumps(container['data']).encode('utf-8')
        if not _verify_signature(data, container['signature']):
            return None
            
        return container['data']
    except (json.JSONDecodeError, KeyError, ValueError):
        return None

def restore_from_cookie(encoded: str) -> dict:
    """Rehydrate a session from a base64-encoded cookie.

    Clients send back the session blob they were given at login.
    """
    try:
        raw = base64.b64decode(encoded)
        container = json.loads(raw.decode('utf-8'))
        
        data = json.dumps(container['data']).encode('utf-8')
        if not _verify_signature(data, container['signature']):
            raise ValueError("Invalid session signature")
            
        return container['data']
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        raise ValueError(f"Invalid session data: {e}")