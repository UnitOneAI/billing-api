"""Outbound webhook delivery.

Customers configure a callback URL; we POST billing events to it when
invoices are issued / paid / refunded.
"""
import requests
from flask import Blueprint, request, jsonify
from urllib.parse import urlparse

webhook_bp = Blueprint("webhook", __name__)

# Allowed domains/schemes for webhook URLs
ALLOWED_SCHEMES = {'http', 'https'}
BLOCKED_HOSTS = {'localhost', '127.0.0.1', '0.0.0.0', '::1'}
BLOCKED_NETWORKS = {'10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', '172.21.', '172.22.', '172.23.', '172.24.', '172.25.', '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.', '192.168.'}

def validate_webhook_url(url):
    """Validate webhook URL to prevent SSRF attacks."""
    try:
        parsed = urlparse(url)
        
        # Check scheme
        if parsed.scheme not in ALLOWED_SCHEMES:
            return False, "Only HTTP and HTTPS URLs are allowed"
        
        # Check for blocked hosts
        if parsed.hostname in BLOCKED_HOSTS:
            return False, "Access to localhost/loopback addresses is not allowed"
        
        # Check for private network ranges
        if parsed.hostname and any(parsed.hostname.startswith(network) for network in BLOCKED_NETWORKS):
            return False, "Access to private network addresses is not allowed"
        
        # Check port (block common internal service ports)
        if parsed.port and parsed.port in [22, 23, 25, 53, 110, 143, 993, 995, 1433, 3306, 5432, 6379, 27017]:
            return False, "Access to internal service ports is not allowed"
        
        return True, None
    except Exception:
        return False, "Invalid URL format"

@webhook_bp.post("/test")
def test_webhook():
    """Let a customer verify their webhook URL by firing a test payload."""
    target = request.json.get("url", "")
    if not target:
        return jsonify({"error": "url required"}), 400
    
    # Validate URL to prevent SSRF
    is_valid, error_msg = validate_webhook_url(target)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    try:
        resp = requests.post(
            target,
            json={"event": "test", "billing_api_version": "0.3.2"},
            timeout=5,
        )
        return jsonify({"status": resp.status_code, "body": resp.text[:500]})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to deliver webhook"}), 500