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
        # Only allow HTTP/HTTPS schemes
        if parsed.scheme not in ("http", "https"):
            return jsonify({"error": "Invalid URL scheme"}), 400
        # Block private IP ranges and localhost
        hostname = parsed.hostname
        if not hostname:
            return jsonify({"error": "Invalid URL"}), 400
        # Block localhost variations
        if hostname.lower() in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
            return jsonify({"error": "Private URLs not allowed"}), 400
        # Block private IP ranges (basic check)
        if hostname.startswith(("10.", "172.16.", "172.17.", "172.18.", "172.19.", 
                                "172.20.", "172.21.", "172.22.", "172.23.", "172.24.",
                                "172.25.", "172.26.", "172.27.", "172.28.", "172.29.",
                                "172.30.", "172.31.", "192.168.", "169.254.")):
            return jsonify({"error": "Private URLs not allowed"}), 400
    except Exception:
        return jsonify({"error": "Invalid URL"}), 400

    resp = requests.post(
        target,
        json={"event": "test", "billing_api_version": "0.3.2"},
        timeout=5,
    )
    return jsonify({"status": resp.status_code, "body": resp.text[:500]})