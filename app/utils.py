import os
import secrets
from urllib.parse import urljoin

from flask import current_app
from werkzeug.utils import secure_filename

import qrcode


def allowed_image(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


def save_uploaded_image(file_storage, folder_key: str) -> str:
    filename = secure_filename(file_storage.filename)
    ext = filename.rsplit(".", 1)[1].lower()
    random_name = f"{secrets.token_hex(12)}.{ext}"

    folder = current_app.config[folder_key]
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, random_name)
    file_storage.save(filepath)

    if folder_key == "UPLOAD_EMPLOYEE_FOLDER":
        return f"uploads/employees/{random_name}"
    return f"uploads/logos/{random_name}"


def build_public_profile_url(public_id: str, request_root: str) -> str:
    base_url = current_app.config.get("PUBLIC_BASE_URL") or request_root
    if not base_url.endswith("/"):
        base_url += "/"
    return urljoin(base_url, f"profile/{public_id}")


def generate_qr_for_employee(public_id: str, request_root: str) -> str:
    data = build_public_profile_url(public_id, request_root)
    qr_img = qrcode.make(data)

    folder = current_app.config["QR_FOLDER"]
    os.makedirs(folder, exist_ok=True)

    filename = f"{public_id}.png"
    path = os.path.join(folder, filename)
    qr_img.save(path)

    return f"uploads/qrcodes/{filename}"
