"""Outbound webhook delivery.

Customers configure a callback URL; we POST billing events to it when
invoices are issued / paid / refunded.
"""
import requests
from flask import Blueprint, request, jsonify
from urllib.parse import urlparse

webhook_bp = Blueprint("webhook", __name__)


def is_safe_url(url):
    """Validate URL to prevent SSRF attacks."""
    try:
        parsed = urlparse(url)
        # Only allow http/https schemes
        if parsed.scheme not in ['http', 'https']:
            return False
        # Block internal/private IP ranges
        hostname = parsed.hostname
        if not hostname:
            return False
        # Block localhost, loopback, and private networks
        if hostname.lower() in ['localhost', '127.0.0.1', '::1']:
            return False
        # Block private IP ranges (simplified check)
        if hostname.startswith(('10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', 
                               '172.21.', '172.22.', '172.23.', '172.24.', '172.25.', 
                               '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', 
                               '172.31.', '192.168.', '169.254.')):
            return False
        return True
    except Exception:
        return False


@webhook_bp.post("/test")
def test_webhook():
    """Let a customer verify their webhook URL by firing a test payload."""
    target = request.json.get("url", "")
    if not target:
        return jsonify({"error": "url required"}), 400
    
    if not is_safe_url(target):
        return jsonify({"error": "invalid or unsafe URL"}), 400

    resp = requests.post(
        target,
        json={"event": "test", "billing_api_version": "0.3.2"},
        timeout=5,
    )
    return jsonify({"status": resp.status_code, "body": resp.text[:500]})