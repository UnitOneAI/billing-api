"""Invoice PDF download."""
import os
from flask import Blueprint, request, send_file, abort

download_bp = Blueprint("download", __name__)

FILE_ROOT = "/var/app/billing/files"


@download_bp.get("/download")
def download():
    """Download an invoice PDF by filename."""
    filename = request.args.get("name", "")
    if not filename:
        abort(400, "name query param required")

    path = os.path.join(FILE_ROOT, filename)
    return send_file(path, as_attachment=True)
