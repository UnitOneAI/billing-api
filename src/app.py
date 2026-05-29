"""Billing API — Flask entrypoint."""
import os
from flask import Flask

from src.auth.login import auth_bp
from src.api.admin import admin_bp
from src.api.users import users_bp
from src.api.invoices import invoices_bp
from src.api.download import download_bp
from src.integrations.webhook import webhook_bp
from src.web.profile import profile_bp
from src.web.redirect import redirect_bp
from src.web.transfer import transfer_bp


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)
    app.testing = testing
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        if testing:
            secret_key = "testing-secret-key-not-for-production"
        else:
            raise RuntimeError("SECRET_KEY environment variable must be set")
    app.secret_key = secret_key

    app.register_blueprint(auth_bp, url_prefix="/auth")
