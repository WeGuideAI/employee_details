# WeGuide Employee ID App

Production-ready Flask application for managing employee profiles, generating QR-linked public ID pages, and showcasing a glassmorphic WeGuide theme.

## Features
- Secure admin login
- Employee CRUD with photo upload
- QR code generation per employee (public profile URL)
- Public profile page accessible via scanned QR code
- Blue and white glassmorphic UI with smooth animations
- Ready for cloud deployment (Railway, Gunicorn + WSGI)

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

## Deploy On Railway
1. Push this repository to GitHub.
2. In Railway, create a new project and select the repo.
3. Railway will use `Dockerfile` + `railway.toml` automatically.
4. Add environment variables in Railway:
- `SECRET_KEY`
- `DATABASE_URL` (PostgreSQL recommended)
- `PUBLIC_BASE_URL` (your production domain)
- `MAX_CONTENT_LENGTH` (bytes, e.g. `16777216` for 16 MB)
- `SESSION_COOKIE_SECURE=true` (for HTTPS)
5. Deploy.
6. Seed admin once (Railway service shell):
   ```bash
   flask seed-admin-from-env
   ```

Health endpoint:
- `GET /healthz`

## Custom Domain Setup (Railway)
1. In Railway service settings, open `Networking` -> `Custom Domain`.
2. Add your domain/subdomain (example: `id.weguide.com`).
3. Create the DNS record Railway asks for (usually `CNAME`).
4. Wait for SSL certificate issuance.
5. Set `PUBLIC_BASE_URL` to your exact HTTPS domain:
   - `PUBLIC_BASE_URL=https://id.weguide.com`

This ensures generated QR codes point to your custom domain.

## Notes
- Uploaded files are stored in `app/static/uploads/`.
- For production, use managed object storage (S3/GCS) instead of local disk.
- Railway ephemeral disk means uploaded files can be lost on redeploy/restart. Move uploads to S3/GCS for production persistence.
