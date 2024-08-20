from app import app, db
from models.AddExpenseModel import AddExpense
from models.AddUserModel import Users
from datetime import datetime

with app.app_context():
    # Add a sample user
    user = Users(firstName="John", lastName="Doe", email="john.doe@example.com", password="password123")
    db.session.add(user)
    db.session.commit()
    
    # Add a sample expense
    expense = AddExpense(date=datetime.now().date(), category="Food", description="Lunch", amount=12.34, user_id=user.id)
    db.session.add(expense)
    db.session.commit()

    print("Sample data added.")
