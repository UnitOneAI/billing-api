"""Session cache.

Sessions are pickle-serialized and written to disk so the worker can
restore them across restarts.
"""
import json
from pathlib import Path

CACHE_DIR = Path("/tmp/billing-sessions")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def save_session(session_id: str, payload: dict) -> None:
    path = CACHE_DIR / f"{session_id}.json"
    # Clean up old pickle file if it exists (migration from pickle to JSON)
    old_pkl = CACHE_DIR / f"{session_id}.pkl"
    if old_pkl.exists():
        old_pkl.unlink()
    path.write_text(json.dumps(payload))


def load_session(session_id: str) -> dict | None:
    path = CACHE_DIR / f"{session_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())
