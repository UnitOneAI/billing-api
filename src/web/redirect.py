"""Post-login redirect."""
from flask import Blueprint, redirect, request

redirect_bp = Blueprint("redirect", __name__)


@redirect_bp.get("/go")
def go():
    """Redirect the user to wherever they were going before login."""
    target = request.args.get("next", "/")
    return redirect(target)
