import os
import secrets

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16))
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/expense_db'  # Use SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
