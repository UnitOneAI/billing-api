"""Outbound webhook delivery.

Customers configure a callback URL; we POST billing events to it when
invoices are issued / paid / refunded.
"""
import requests
from flask import Blueprint, request, jsonify

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.post("/test")
def test_webhook():
    """Let a customer verify their webhook URL by firing a test payload."""
    target = request.json.get("url", "")
    if not target:
        return jsonify({"error": "url required"}), 400

    resp = requests.post(
        target,
        json={"event": "test", "billing_api_version": "0.3.2"},
        timeout=5,
    )
    return jsonify({"status": resp.status_code, "body": resp.text[:500]})
