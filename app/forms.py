from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, EmailField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log In")


class EmployeeForm(FlaskForm):
    employee_code = StringField("Employee ID", validators=[DataRequired(), Length(max=50)])
    full_name = StringField("Full Name", validators=[DataRequired(), Length(max=120)])
    designation = StringField("Designation", validators=[DataRequired(), Length(max=120)])
    department = StringField("Department", validators=[Optional(), Length(max=120)])
    blood_group = StringField("Blood Group", validators=[Optional(), Length(max=8)])
    address = TextAreaField("Address", validators=[Optional(), Length(max=1000)])
    phone_number = StringField("Phone Number", validators=[Optional(), Length(max=30)])
    email = EmailField("Email", validators=[Optional(), Email(), Length(max=255)])
    emergency_contact = StringField("Emergency Contact", validators=[Optional(), Length(max=120)])
    date_of_birth = DateField("Date of Birth", validators=[Optional()], format="%Y-%m-%d")
    date_of_joining = DateField("Date of Joining", validators=[Optional()], format="%Y-%m-%d")
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save Employee")
