import os
from pathlib import Path

from flask import Flask, current_app
from werkzeug.middleware.proxy_fix import ProxyFix

from app.config import config_by_name
from app.extensions import csrf, db, login_manager


def create_app(config_name: str = "production") -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    Path(app.config["UPLOAD_EMPLOYEE_FOLDER"]).mkdir(parents=True, exist_ok=True)
    Path(app.config["UPLOAD_LOGO_FOLDER"]).mkdir(parents=True, exist_ok=True)
    Path(app.config["QR_FOLDER"]).mkdir(parents=True, exist_ok=True)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    from app.models import AdminUser
    from app.utils import media_url

    @login_manager.user_loader
    def load_user(user_id: str):
        return AdminUser.query.get(int(user_id))

    @app.context_processor
    def inject_media_helpers():
        return {"media_url": media_url}

    from app.auth.routes import auth_bp
    from app.admin.routes import admin_bp
    from app.public.routes import public_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(public_bp)

    register_cli_commands(app)
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}, 200

    return app


def register_cli_commands(app: Flask) -> None:
    import click
    from werkzeug.security import generate_password_hash

    from app.extensions import db
    from app.models import AdminUser

    @app.cli.command("create-admin")
    @click.option("--email", required=True, help="Admin email")
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    def create_admin(email: str, password: str):
        if AdminUser.query.filter_by(email=email.lower().strip()).first():
            click.echo("Admin already exists with this email.")
            return

        admin = AdminUser(email=email.lower().strip(), password_hash=generate_password_hash(password))
        db.session.add(admin)
        db.session.commit()
        click.echo("Admin created successfully.")


    @app.cli.command("seed-admin-from-env")
    def seed_admin_from_env():
        from werkzeug.security import generate_password_hash

        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")
        if not email or not password:
            click.echo("Set ADMIN_EMAIL and ADMIN_PASSWORD first.")
            return

        if AdminUser.query.filter_by(email=email.lower().strip()).first():
            click.echo("Admin already exists.")
            return

        user = AdminUser(email=email.lower().strip(), password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        click.echo("Admin seeded successfully.")


def register_error_handlers(app: Flask) -> None:
    from flask import render_template

    @app.errorhandler(413)
    def payload_too_large(_):
        return render_template("errors/413.html"), 413

    @app.errorhandler(404)
    def not_found(_):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(_):
        if current_app:
            db.session.rollback()
        return render_template("errors/500.html"), 500
