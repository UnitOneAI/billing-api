    return render_template_string("""
    <html>
      <body>
        <h1>Welcome, {{ name|e }}!</h1>
        <p>Your billing profile is up to date.</p>
      </body>
    </html>
    """, name=name)