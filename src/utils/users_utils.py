from models import Users

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
