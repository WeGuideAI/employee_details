# WeGuide Employee ID App

Production-ready Flask application for managing employee profiles, generating QR-linked public ID pages, and showcasing a glassmorphic WeGuide theme.

## Features
- Secure admin login
- Employee CRUD with photo upload
- Company settings with rectangular logo upload
- QR code generation per employee (public profile URL)
- Public profile page accessible via scanned QR code
- Blue and white glassmorphic UI with smooth animations
- Ready for cloud deployment (Gunicorn + WSGI)

## Quick Start
1. Create virtualenv and install dependencies:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. Configure environment:
   ```powershell
   copy .env.example .env
   ```
3. Set Flask app and initialize DB:
   ```powershell
   $env:FLASK_APP = "run.py"
   flask create-admin --email admin@weguide.com
   ```
4. Run app:
   ```powershell
   python run.py
   ```
5. Login at:
   `http://127.0.0.1:5000/login`

## Deploy
Use Gunicorn in Linux cloud environments:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

Set these environment variables in cloud:
- `SECRET_KEY`
- `DATABASE_URL` (PostgreSQL recommended)
- `PUBLIC_BASE_URL` (your production domain)
- `MAX_CONTENT_LENGTH` (bytes, e.g. `16777216` for 16 MB)
- `SESSION_COOKIE_SECURE=true` (for HTTPS)

## Notes
- Uploaded files are stored in `app/static/uploads/`.
- For production, use managed object storage (S3/GCS) instead of local disk.
- If you use Nginx, set `client_max_body_size 16M;` (or higher) to match Flask upload limits.
