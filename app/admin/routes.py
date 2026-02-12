from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.extensions import db
from app.forms import EmployeeForm
from app.models import Employee
from app.utils import allowed_image, generate_qr_for_employee, save_uploaded_image


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    employees = Employee.query.order_by(Employee.created_at.desc()).all()
    return render_template("admin/dashboard.html", employees=employees)


@admin_bp.route("/employees/new", methods=["GET", "POST"])
@login_required
def create_employee():
    form = EmployeeForm()

    if form.validate_on_submit():
        existing = Employee.query.filter_by(employee_code=form.employee_code.data.strip()).first()
        if existing:
            flash("Employee ID already exists.", "danger")
            return render_template("admin/employee_form.html", form=form, mode="create")

        employee = Employee(
            employee_code=form.employee_code.data.strip(),
            full_name=form.full_name.data.strip(),
            designation=form.designation.data.strip(),
            department=(form.department.data or "").strip() or None,
            blood_group=(form.blood_group.data or "").strip() or None,
            address=(form.address.data or "").strip() or None,
            phone_number=(form.phone_number.data or "").strip() or None,
            email=(form.email.data or "").strip().lower() or None,
            emergency_contact=(form.emergency_contact.data or "").strip() or None,
            date_of_birth=form.date_of_birth.data,
            date_of_joining=form.date_of_joining.data,
            is_active=form.is_active.data,
        )

        photo = request.files.get("photo")
        if photo and photo.filename:
            if not allowed_image(photo.filename):
                flash("Unsupported image format.", "danger")
                return render_template("admin/employee_form.html", form=form, mode="create")
            employee.photo_path = save_uploaded_image(photo, "UPLOAD_EMPLOYEE_FOLDER")

        db.session.add(employee)
        db.session.flush()
        employee.qr_code_path = generate_qr_for_employee(employee.public_id, request.url_root)

        db.session.commit()
        flash("Employee created successfully.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/employee_form.html", form=form, mode="create")


@admin_bp.route("/employees/<int:employee_id>/edit", methods=["GET", "POST"])
@login_required
def edit_employee(employee_id: int):
    employee = Employee.query.get_or_404(employee_id)
    form = EmployeeForm(obj=employee)

    if form.validate_on_submit():
        duplicate = Employee.query.filter(Employee.employee_code == form.employee_code.data.strip(), Employee.id != employee.id).first()
        if duplicate:
            flash("Employee ID already exists.", "danger")
            return render_template("admin/employee_form.html", form=form, mode="edit", employee=employee)

        employee.employee_code = form.employee_code.data.strip()
        employee.full_name = form.full_name.data.strip()
        employee.designation = form.designation.data.strip()
        employee.department = (form.department.data or "").strip() or None
        employee.blood_group = (form.blood_group.data or "").strip() or None
        employee.address = (form.address.data or "").strip() or None
        employee.phone_number = (form.phone_number.data or "").strip() or None
        employee.email = (form.email.data or "").strip().lower() or None
        employee.emergency_contact = (form.emergency_contact.data or "").strip() or None
        employee.date_of_birth = form.date_of_birth.data
        employee.date_of_joining = form.date_of_joining.data
        employee.is_active = form.is_active.data

        photo = request.files.get("photo")
        if photo and photo.filename:
            if not allowed_image(photo.filename):
                flash("Unsupported image format.", "danger")
                return render_template("admin/employee_form.html", form=form, mode="edit", employee=employee)
            employee.photo_path = save_uploaded_image(photo, "UPLOAD_EMPLOYEE_FOLDER")

        employee.qr_code_path = generate_qr_for_employee(employee.public_id, request.url_root)

        db.session.commit()
        flash("Employee updated.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/employee_form.html", form=form, mode="edit", employee=employee)


@admin_bp.route("/employees/<int:employee_id>/delete", methods=["POST"])
@login_required
def delete_employee(employee_id: int):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash("Employee deleted.", "info")
    return redirect(url_for("admin.dashboard"))

