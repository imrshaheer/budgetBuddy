from datetime import datetime, timedelta
from models import AddExpense

def get_expenses_summary(user_id):
    """Fetch and summarize expenses for various periods."""
    return {
        'today_expenses': expenses_today(user_id),
        'yesterday_expenses': expenses_yesterday(user_id),
        'last_7_days_expenses': expenses_last_7_days(user_id),
        'current_month_expenses': expenses_current_month(user_id),
        'one_year_expenses': expenses_last_year(user_id),
        'total_expenses': total_expenses(user_id)
    }

def format_currency(amount):
    """Format amount in PKR currency format."""
    return f'PKR {amount:,.1f}'

def expenses_today(user_id):
    """Calculate total expenses for today."""
    today = datetime.now().date()
    return calculate_expenses(user_id=user_id, start_date=today, end_date=today)

def expenses_yesterday(user_id):
    """Calculate total expenses for yesterday."""
    yesterday = datetime.now().date() - timedelta(days=1)
    return calculate_expenses(user_id=user_id, start_date=yesterday, end_date=yesterday)

def expenses_last_7_days(user_id):
    """Calculate total expenses for the last 7 days."""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    return calculate_expenses(user_id=user_id, start_date=start_date, end_date=end_date)

def expenses_current_month(user_id):
    """Calculate total expenses for the current month."""
    end_date = datetime.now().date()
    start_date = end_date.replace(day=1)
    return calculate_expenses(user_id=user_id, start_date=start_date, end_date=end_date)

def expenses_last_year(user_id):
    """Calculate total expenses for the current year."""
    current_year = datetime.now().year
    start_date = datetime(current_year, 1, 1).date()
    end_date = datetime(current_year + 1, 1, 1).date()
    return calculate_expenses(user_id=user_id, start_date=start_date, end_date=end_date)

def total_expenses(user_id):
    """Calculate total expenses for all time."""
    return calculate_expenses(user_id=user_id)

def calculate_expenses(user_id=None, start_date=None, end_date=None):
    """Calculate total expenses within the given date range for a specific user."""
    query = AddExpense.query
    
    if user_id:
        query = query.filter_by(user_id=user_id)   
    if start_date and end_date:
        query = query.filter(AddExpense.date.between(start_date, end_date))
    
    expenses = query.all()
    
    return sum(int(expense.amount) for expense in expenses)
