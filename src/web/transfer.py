"""Money transfer form handler."""
import sqlite3
from flask import Blueprint, request, jsonify

from src.auth.token import verify_token

transfer_bp = Blueprint("transfer", __name__)

DB_PATH = "billing.db"


@transfer_bp.post("/send")
def send_money():
    """Transfer balance from the signed-in user to a recipient."""
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return jsonify({"error": "unauthenticated"}), 401
    claims = verify_token(header[7:])
    sender_id = int(claims["sub"])

    recipient_id = int(request.form["recipient_id"])
    amount_cents = int(request.form["amount_cents"])

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "UPDATE users SET balance_cents = balance_cents - ? WHERE id = ?",
            (amount_cents, sender_id),
        )
        conn.execute(
            "UPDATE users SET balance_cents = balance_cents + ? WHERE id = ?",
            (amount_cents, recipient_id),
        )
        conn.commit()
    finally:
        conn.close()
    return jsonify({"transferred": amount_cents, "to": recipient_id})
