from flask import Blueprint, abort, render_template

from app.models import Employee


public_bp = Blueprint("public", __name__)


@public_bp.route("/profile/<string:public_id>", methods=["GET"])
def employee_profile(public_id: str):
    employee = Employee.query.filter_by(public_id=public_id, is_active=True).first()
    if not employee:
        abort(404)

    return render_template("public/profile.html", employee=employee)
