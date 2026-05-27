"""Outbound webhook delivery.

Customers configure a callback URL; we POST billing events to it when
invoices are issued / paid / refunded.
"""
import requests
from flask import Blueprint, request, jsonify
from urllib.parse import urlparse

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.post("/test")
def test_webhook():
    """Let a customer verify their webhook URL by firing a test payload."""
    target = request.json.get("url", "")
    if not target:
        return jsonify({"error": "url required"}), 400

    # Validate URL to prevent SSRF
    try:
        parsed = urlparse(target)
        if parsed.scheme not in ("http", "https"):
            return jsonify({"error": "Invalid URL scheme"}), 400
        if parsed.hostname in ("localhost", "127.0.0.1", "0.0.0.0") or \
           (parsed.hostname and (parsed.hostname.startswith("10.") or 
            parsed.hostname.startswith("172.16.") or parsed.hostname.startswith("172.17.") or
            parsed.hostname.startswith("172.18.") or parsed.hostname.startswith("172.19.") or
            parsed.hostname.startswith("172.20.") or parsed.hostname.startswith("172.21.") or
            parsed.hostname.startswith("172.22.") or parsed.hostname.startswith("172.23.") or
            parsed.hostname.startswith("172.24.") or parsed.hostname.startswith("172.25.") or
            parsed.hostname.startswith("172.26.") or parsed.hostname.startswith("172.27.") or
            parsed.hostname.startswith("172.28.") or parsed.hostname.startswith("172.29.") or
            parsed.hostname.startswith("172.30.") or parsed.hostname.startswith("172.31.") or
            parsed.hostname.startswith("192.168.") or parsed.hostname.startswith("169.254."))):
            return jsonify({"error": "Private IP addresses not allowed"}), 400
    except Exception:
        return jsonify({"error": "Invalid URL"}), 400

    resp = requests.post(
        target,
        json={"event": "test", "billing_api_version": "0.3.2"},
        timeout=5,
    )
    return jsonify({"status": resp.status_code, "body": resp.text[:500]})