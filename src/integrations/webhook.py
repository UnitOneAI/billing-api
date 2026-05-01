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
    
    # Validate URL to prevent SSRF attacks
    try:
        parsed = urlparse(target)
        if not parsed.scheme or parsed.scheme not in ['http', 'https']:
            return jsonify({"error": "Invalid URL scheme"}), 400
        if not parsed.hostname:
            return jsonify({"error": "Invalid URL hostname"}), 400
        # Block localhost, private IPs, and common internal addresses
        if parsed.hostname.lower() in ['localhost', '127.0.0.1', '::1'] or \
           parsed.hostname.startswith('192.168.') or \
           parsed.hostname.startswith('10.') or \
           (parsed.hostname.startswith('172.') and 
            16 <= int(parsed.hostname.split('.')[1]) <= 31) or \
           parsed.hostname.startswith('169.254.') or \
           parsed.hostname.endswith('.local'):
            return jsonify({"error": "URL not allowed"}), 400
    except (ValueError, IndexError):
        return jsonify({"error": "Invalid URL format"}), 400

    resp = requests.post(
        target,
        json={"event": "test", "billing_api_version": "0.3.2"},
        timeout=5,
    )
    return jsonify({"status": resp.status_code, "body": resp.text[:500]})