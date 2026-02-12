from datetime import datetime
import uuid

from flask_login import UserMixin

from app.extensions import db


class AdminUser(UserMixin, db.Model):
    __tablename__ = "admin_users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class CompanySettings(db.Model):
    __tablename__ = "company_settings"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120), default="WeGuide", nullable=False)
    logo_path = db.Column(db.String(255), nullable=True)
    primary_color = db.Column(db.String(20), default="#0F4DFF", nullable=False)
    secondary_color = db.Column(db.String(20), default="#EAF2FF", nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    employee_code = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    designation = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120), nullable=True)
    blood_group = db.Column(db.String(8), nullable=True)
    address = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    emergency_contact = db.Column(db.String(120), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    date_of_joining = db.Column(db.Date, nullable=True)
    photo_path = db.Column(db.String(255), nullable=True)
    qr_code_path = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
