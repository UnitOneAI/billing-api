"""Outbound webhook delivery.

Customers configure a callback URL; we POST billing events to it when
invoices are issued / paid / refunded.
"""
import requests
from flask import Blueprint, request, jsonify
from urllib.parse import urlparse

webhook_bp = Blueprint("webhook", __name__)

# Allowed URL schemes and domains for webhook testing
ALLOWED_SCHEMES = {'http', 'https'}
BLOCKED_HOSTS = {
    'localhost', '127.0.0.1', '0.0.0.0', '::1',
    '169.254.169.254',  # AWS metadata service
    '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16'  # Private networks
}

def is_safe_url(url):
    """Validate that the URL is safe for outbound requests."""
    try:
        parsed = urlparse(url)
        
        # Check scheme
        if parsed.scheme not in ALLOWED_SCHEMES:
            return False
            
        # Check for blocked hosts
        hostname = parsed.hostname
        if not hostname:
            return False
            
        # Block localhost and private networks
        if hostname.lower() in BLOCKED_HOSTS:
            return False
            
        # Block IP addresses in private ranges
        import ipaddress
        try:
            ip = ipaddress.ip_address(hostname)
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                return False
        except ValueError:
            # Not an IP address, continue with hostname validation
            pass
            
        return True
    except Exception:
        return False


@webhook_bp.post("/test")
def test_webhook():
    """Let a customer verify their webhook URL by firing a test payload."""
    target = request.json.get("url", "")
    if not target:
        return jsonify({"error": "url required"}), 400

    # Validate URL to prevent SSRF attacks
    if not is_safe_url(target):
        return jsonify({"error": "Invalid or unsafe URL"}), 400

    try:
        resp = requests.post(
            target,
            json={"event": "test", "billing_api_version": "0.3.2"},
            timeout=5,
        )
        return jsonify({"status": resp.status_code, "body": resp.text[:500]})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request failed"}), 500