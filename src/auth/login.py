"""Login handlers backed by SQLite."""
import sqlite3
from flask import Blueprint, request, jsonify

from src.auth.hash import hash_password
from src.auth.token import issue_token

auth_bp = Blueprint("auth", __name__)

DB_PATH = "billing.db"


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


@auth_bp.post("/login")
def login():
    """Authenticate a user by username/password."""
    username = request.json.get("username", "")
    password = request.json.get("password", "")
    hashed = hash_password(password)

    query = (
        "SELECT id, email, is_admin FROM users "
        "WHERE username = ? AND password_hash = ?"
    )

    conn = _connect()
    try:
        row = conn.execute(query, (username, hashed)).fetchone()
    finally:
        conn.close()

    if not row:
        return jsonify({"error": "invalid credentials"}), 401

    user_id, email, is_admin = row
    token = issue_token(user_id=user_id, email=email, is_admin=bool(is_admin))
    return jsonify({"token": token, "user_id": user_id})