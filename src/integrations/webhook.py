"""Outbound webhook delivery.

Customers configure a callback URL; we POST billing events to it when
invoices are issued / paid / refunded.
"""
import requests
from flask import Blueprint, request, jsonify
from urllib.parse import urlparse

webhook_bp = Blueprint("webhook", __name__)

# Allowed domains/schemes for webhook URLs
ALLOWED_SCHEMES = {'https'}
BLOCKED_HOSTS = {
    'localhost', '127.0.0.1', '0.0.0.0', '::1',
    '169.254.169.254',  # AWS metadata service
    '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16'  # Private networks
}

def is_safe_url(url):
    """Validate that the URL is safe for webhook delivery."""
    try:
        parsed = urlparse(url)
        
        # Only allow HTTPS
        if parsed.scheme not in ALLOWED_SCHEMES:
            return False
            
        # Block localhost and private IPs
        hostname = parsed.hostname
        if not hostname:
            return False
            
        # Check against blocked hosts
        if hostname.lower() in BLOCKED_HOSTS:
            return False
            
        # Block private IP ranges (basic check)
        if (hostname.startswith('10.') or 
            hostname.startswith('192.168.') or 
            hostname.startswith('172.')):
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
    
    # Validate URL to prevent SSRF
    if not is_safe_url(target):
        return jsonify({"error": "Invalid or unsafe URL provided"}), 400

    try:
        resp = requests.post(
            target,
            json={"event": "test", "billing_api_version": "0.3.2"},
            timeout=5,
        )
        return jsonify({"status": resp.status_code, "body": resp.text[:500]})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to deliver webhook"}), 500