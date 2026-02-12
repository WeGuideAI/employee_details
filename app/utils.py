import os
import secrets
from io import BytesIO
from urllib.parse import urljoin

from flask import current_app, url_for
from werkzeug.utils import secure_filename

import qrcode


def allowed_image(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


def save_uploaded_image(file_storage, folder_key: str) -> str:
    if should_use_cloudinary():
        return upload_to_cloudinary(
            file_storage=file_storage,
            folder="weguide/employees",
            public_id=f"employee_{secrets.token_hex(10)}",
        )

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

    if should_use_cloudinary():
        qr_bytes = BytesIO()
        qr_img.save(qr_bytes, format="PNG")
        qr_bytes.seek(0)
        return upload_to_cloudinary(
            file_storage=qr_bytes,
            folder="weguide/qrcodes",
            public_id=f"qr_{public_id}",
            overwrite=True,
            resource_type="image",
            format="png",
        )

    folder = current_app.config["QR_FOLDER"]
    os.makedirs(folder, exist_ok=True)

    filename = f"{public_id}.png"
    path = os.path.join(folder, filename)
    qr_img.save(path)

    return f"uploads/qrcodes/{filename}"


def should_use_cloudinary() -> bool:
    cfg = current_app.config
    return bool(
        cfg.get("USE_CLOUDINARY")
        and cfg.get("CLOUDINARY_CLOUD_NAME")
        and cfg.get("CLOUDINARY_API_KEY")
        and cfg.get("CLOUDINARY_API_SECRET")
    )


def upload_to_cloudinary(
    file_storage,
    folder: str,
    public_id: str,
    overwrite: bool = False,
    resource_type: str = "image",
    format: str | None = None,
) -> str:
    import cloudinary
    import cloudinary.uploader

    cfg = current_app.config
    cloudinary.config(
        cloud_name=cfg["CLOUDINARY_CLOUD_NAME"],
        api_key=cfg["CLOUDINARY_API_KEY"],
        api_secret=cfg["CLOUDINARY_API_SECRET"],
        secure=True,
    )

    upload_result = cloudinary.uploader.upload(
        file_storage,
        folder=folder,
        public_id=public_id,
        overwrite=overwrite,
        resource_type=resource_type,
        format=format,
    )
    return upload_result["secure_url"]


def media_url(path: str | None) -> str:
    if not path:
        return ""
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return url_for("static", filename=path)
