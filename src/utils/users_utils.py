from models import Users
from flask import session

def is_logged_in():
    return 'user_id' in session

def validate_registration_data(fname, lname, email, password, repeat_password):
    if not (fname and lname and email and password and repeat_password):
        return "Please fill out all fields."
    if password != repeat_password:
        return "Passwords do not match. Please try again."
    if Users.query.filter_by(email=email).first():
        return "Email is already registered. Please login."
    return None

def get_user_by_email_and_password(email, password):
    """Fetch the user by email and password"""
    return Users.query.filter_by(email=email, password=password).first()

def get_user_by_email(email):
    """Fetch the user by email"""
    return Users.query.filter_by(email=email).first()

def get_user_full_name(user_id):
    user = Users.query.get(user_id)
    if user:
        user_name = f"{user.first_name} {user.last_name}"
        return user_name
    return None
