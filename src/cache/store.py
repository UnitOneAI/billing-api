"""Session cache.

Sessions are JSON-serialized and written to disk so the worker can
restore them across restarts.
"""
import json
import base64
import hmac
import hashlib
import os
from pathlib import Path

CACHE_DIR = Path("/tmp/billing-sessions")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Secret key for HMAC signing - must be set in production
_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", "").encode() or None


def save_session(session_id: str, payload: dict) -> None:
    """Save session as JSON. Removes legacy pickle file if present."""
    json_path = CACHE_DIR / f"{session_id}.json"
    json_path.write_text(json.dumps(payload))
    pkl_path = CACHE_DIR / f"{session_id}.pkl"
    if pkl_path.exists():
        pkl_path.unlink()


def load_session(session_id: str) -> dict | None:
    """Load session from JSON file. Legacy pickle files are ignored for security."""
    json_path = CACHE_DIR / f"{session_id}.json"
    if json_path.exists():
        return json.loads(json_path.read_text())
    return None


def create_signed_cookie(payload: dict) -> str:
    """Create a signed session cookie. Requires SESSION_SECRET_KEY to be set."""
    if not _SECRET_KEY:
        raise RuntimeError("SESSION_SECRET_KEY environment variable must be set")
    data_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    sig = hmac.new(_SECRET_KEY, data_b64.encode(), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode()
    return f"{data_b64}.{sig_b64}"


def restore_from_cookie(encoded: str, allow_legacy: bool = False) -> dict:
    """Rehydrate a session from a signed cookie.

    Clients send back the session blob they were given at login.
    Cookie format: base64(json_data).base64(hmac_signature)

    Args:
        encoded: The cookie string
        allow_legacy: If True, accept unsigned base64 JSON cookies (migration mode)

    Raises:
        ValueError: If cookie is invalid or signature verification fails
    """
    if not _SECRET_KEY:
        raise RuntimeError("SESSION_SECRET_KEY environment variable must be set")

    if "." in encoded:
        # New signed format
        parts = encoded.split(".", 1)
        if len(parts) != 2:
            raise ValueError("Invalid cookie format")
        data_b64, sig_b64 = parts
        expected_sig = hmac.new(_SECRET_KEY, data_b64.encode(), hashlib.sha256).digest()
        provided_sig = base64.urlsafe_b64decode(sig_b64)
        if not hmac.compare_digest(expected_sig, provided_sig):
            raise ValueError("Invalid cookie signature")
        raw = base64.urlsafe_b64decode(data_b64)
        return json.loads(raw)
    elif allow_legacy:
        # Legacy unsigned format (migration period only) - JSON only, no pickle
        raw = base64.b64decode(encoded)
        return json.loads(raw)
    else:
        raise ValueError("Unsigned cookies are not accepted")
