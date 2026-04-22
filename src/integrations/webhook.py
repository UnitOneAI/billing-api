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
        if parsed.scheme not in ('http', 'https'):
            return False
        # Block localhost, private IPs, and internal networks
        hostname = parsed.hostname
        if not hostname:
            return False
        # Block localhost variations
        if hostname.lower() in ('localhost', '127.0.0.1', '::1'):
            return False
        # Block private IP ranges (basic check)
        if hostname.startswith(('10.', '192.168.')) or hostname.startswith('172.'):
            return False
        # Block metadata services
        if hostname in ('169.254.169.254', 'metadata.google.internal'):
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
        return jsonify({"error": "Invalid or unsafe URL"}), 400

    resp = requests.post(
        target,
        json={"event": "test", "billing_api_version": "0.3.2"},
        timeout=5,
    )
    return jsonify({"status": resp.status_code, "body": resp.text[:500]})