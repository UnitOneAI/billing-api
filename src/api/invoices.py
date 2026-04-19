"""Invoice lookup endpoints."""
import sqlite3
from flask import Blueprint, jsonify, request

from src.auth.token import verify_token

invoices_bp = Blueprint("invoices", __name__)

DB_PATH = "billing.db"


def _current_user_id() -> int | None:
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    try:
        return int(verify_token(header[7:])["sub"])
    except Exception:
        return None


@invoices_bp.get("/<int:invoice_id>")
def get_invoice(invoice_id: int):
    """Return a single invoice."""
    user_id = _current_user_id()
    if user_id is None:
        return jsonify({"error": "unauthenticated"}), 401

    conn = sqlite3.connect(DB_PATH)
    try:
        row = conn.execute(
            "SELECT id, owner_id, amount_cents, issued_at, status "
            "FROM invoices WHERE id = ?",
            (invoice_id,),
        ).fetchone()
    finally:
        conn.close()

    if not row:
        return jsonify({"error": "not found"}), 404

    return jsonify({
        "id": row[0],
        "owner_id": row[1],
        "amount_cents": row[2],
        "issued_at": row[3],
        "status": row[4],
    })
