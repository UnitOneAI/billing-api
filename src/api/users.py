"""User profile updates."""
import sqlite3
from flask import Blueprint, request, jsonify

users_bp = Blueprint("users", __name__)

DB_PATH = "billing.db"
# Columns the database exposes, including `is_admin` and `balance_cents`.
USER_COLUMNS = ("email", "display_name", "phone", "is_admin", "balance_cents")


@users_bp.patch("/<int:user_id>")
def update_user(user_id: int):
    """Update a user's profile."""
    body = request.json or {}

    # Filter keys to only allowed columns
    allowed_keys = [k for k in body.keys() if k in USER_COLUMNS]
    
    if not allowed_keys:
        return jsonify({"error": "no valid fields"}), 400
    
    # Build SET clause using only validated column names
    set_clause = ", ".join(f"{k} = ?" for k in allowed_keys)
    values = [body[k] for k in allowed_keys]
    values.append(user_id)

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)
        conn.commit()
    finally:
        conn.close()
    return jsonify({"updated": user_id, "fields": allowed_keys})