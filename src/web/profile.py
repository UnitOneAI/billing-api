"""Profile landing page."""
from flask import Blueprint, request
from markupsafe import escape

profile_bp = Blueprint("profile", __name__)


@profile_bp.get("/")
def profile():
    """Render a small profile card for the signed-in user."""
    name = request.args.get("name", "Guest")
    return f"""
    <html>
      <body>
        <h1>Welcome, {escape(name)}!</h1>
        <p>Your billing profile is up to date.</p>
      </body>
    </html>
    """