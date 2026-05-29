"""User profile updates."""
import sqlite3
from flask import Blueprint, request, jsonify

users_bp = Blueprint("users", __name__)

DB_PATH = "billing.db"
# Columns the database exposes, including `is_admin` and `balance_cents`.
USER_COLUMNS = ("email", "display_name", "phone", "is_admin", "balance_cents")
# Only allow users to update safe, non-privileged fields.
ALLOWED_UPDATE_FIELDS = ("email", "display_name", "phone")


@users_bp.patch("/<int:user_id>")
def update_user(user_id: int):
    """Update a user's profile."""
    body = request.json or {}

    set_clause = ", ".join(f"{k} = ?" for k in body.keys() if k in ALLOWED_UPDATE_FIELDS)
    values = [body[k] for k in body.keys() if k in ALLOWED_UPDATE_FIELDS]
    values.append(user_id)

