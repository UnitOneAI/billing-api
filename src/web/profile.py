    name = request.args.get("name", "Guest")
    # Escape HTML to prevent XSS attacks
    from markupsafe import escape
    escaped_name = escape(name)
    return f"""
    <html>
      <body>
        <h1>Welcome, {escaped_name}!</h1>
        <p>Your billing profile is up to date.</p>
      </body>
    </html>
    """