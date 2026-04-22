    # Validate URL to prevent SSRF attacks
    from urllib.parse import urlparse
    
    try:
        parsed_url = urlparse(target)
        # Only allow HTTP/HTTPS schemes
        if parsed_url.scheme not in ['http', 'https']:
            return jsonify({"error": "Invalid URL scheme. Only HTTP and HTTPS are allowed."}), 400
        
        # Block private/internal IP ranges
        hostname = parsed_url.hostname
        if not hostname:
            return jsonify({"error": "Invalid URL format."}), 400
            
        import ipaddress
        try:
            ip = ipaddress.ip_address(hostname)
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                return jsonify({"error": "Access to private IP ranges is not allowed."}), 400
        except ValueError:
            # hostname is not an IP address, check for localhost/private domains
            if hostname.lower() in ['localhost', '127.0.0.1', '0.0.0.0'] or hostname.startswith('10.') or hostname.startswith('192.168.') or hostname.startswith('172.'):
                return jsonify({"error": "Access to private networks is not allowed."}), 400
    except Exception:
        return jsonify({"error": "Invalid URL format."}), 400

    resp = requests.post(
        target,
        json={"event": "test", "billing_api_version": "0.3.2"},
        timeout=5,
    )