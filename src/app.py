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


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", os.urandom(32).hex())

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(invoices_bp, url_prefix="/api/invoices")
    app.register_blueprint(download_bp, url_prefix="/api/files")
    app.register_blueprint(webhook_bp, url_prefix="/webhooks")
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(redirect_bp)
    app.register_blueprint(transfer_bp, url_prefix="/transfer")

    @app.get("/healthz")
    def healthz():
        return {"status": "ok", "version": "0.3.2"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)