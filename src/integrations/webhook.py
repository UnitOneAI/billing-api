"""Outbound webhook delivery.

Customers configure a callback URL; we POST billing events to it when
invoices are issued / paid / refunded.
"""
import requests
from flask import Blueprint, request, jsonify
from urllib.parse import urlparse

webhook_bp = Blueprint("webhook", __name__)

# Allowed protocols and domains for webhook URLs
ALLOWED_PROTOCOLS = {'http', 'https'}
PRIVATE_IP_RANGES = [
    '127.0.0.0/8',    # loopback
    '10.0.0.0/8',     # private class A
    '172.16.0.0/12',  # private class B  
    '192.168.0.0/16', # private class C
    '169.254.0.0/16', # link-local
    'fc00::/7',       # IPv6 private
    '::1/128'         # IPv6 loopback
]

def is_safe_url(url):
    """Validate that URL is safe for webhook requests."""
    try:
        parsed = urlparse(url)
        
        # Check protocol
        if parsed.scheme.lower() not in ALLOWED_PROTOCOLS:
            return False
            
        # Check for valid hostname
        if not parsed.hostname:
            return False
            
        # Prevent requests to private/internal networks
        import ipaddress
        try:
            ip = ipaddress.ip_address(parsed.hostname)
            for private_range in PRIVATE_IP_RANGES:
                if '/' in private_range:
                    if ip in ipaddress.ip_network(private_range, strict=False):
                        return False
                        
        except ValueError:
            # hostname is not an IP, check for localhost/internal domains
            hostname = parsed.hostname.lower()
            if hostname in ['localhost', 'metadata.google.internal'] or hostname.endswith('.local'):
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
        return jsonify({"error": "Invalid or unsafe URL"}), 400

    try:
        resp = requests.post(
            target,
            json={"event": "test", "billing_api_version": "0.3.2"},
            timeout=5,
        )
        return jsonify({"status": resp.status_code, "body": resp.text[:500]})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request failed"}), 400