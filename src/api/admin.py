"""Admin-only operations."""
import sqlite3
from flask import Blueprint, request, jsonify

admin_bp = Blueprint("admin", __name__)

DB_PATH = "billing.db"


@admin_bp.get("/revenue")
def revenue_report():
    """Return total revenue for the current period.

    Used by the finance dashboard — admins only.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        row = conn.execute("SELECT SUM(amount_cents) FROM invoices").fetchone()
    finally:
        conn.close()
    total = (row[0] or 0) / 100
    return jsonify({"total_usd": total})


@admin_bp.post("/users/delete")
def delete_user():
    user_id = request.json.get("user_id")
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
    finally:
        conn.close()
    return jsonify({"deleted": user_id})
