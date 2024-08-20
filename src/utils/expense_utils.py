from datetime import datetime, timedelta
from models.AddExpenseModel import AddExpense

def get_expenses_summary():
    """Fetch and summarize expenses for various periods."""
    return {
        'today_expenses': expenses_today(),
        'yesterday_expenses': expenses_yesterday(),
        'last_7_days_expenses': expenses_last_7_days(),
        'current_month_expenses': expenses_current_month(),
        'one_year_expenses': expenses_last_year(),
        'total_expenses': total_expenses()
    }

def format_currency(amount):
    """Format amount in PKR currency format."""
    return f'PKR {amount:,.1f}'

def expenses_today():
    """Calculate total expenses for today."""
    today = datetime.now().date()
    return calculate_expenses(start_date=today, end_date=today)

def expenses_yesterday():
    """Calculate total expenses for yesterday."""
    yesterday = datetime.now().date() - timedelta(days=1)
    return calculate_expenses(start_date=yesterday, end_date=yesterday)

def expenses_last_7_days():
    """Calculate total expenses for the last 7 days."""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    return calculate_expenses(start_date=start_date, end_date=end_date)

def expenses_current_month():
    """Calculate total expenses for the current month."""
    end_date = datetime.now().date()
    start_date = end_date.replace(day=1)
    return calculate_expenses(start_date=start_date, end_date=end_date)

def expenses_last_year():
    """Calculate total expenses for the current year."""
    current_year = datetime.now().year
    start_date = datetime(current_year, 1, 1).date()
    end_date = datetime(current_year + 1, 1, 1).date()
    return calculate_expenses(start_date=start_date, end_date=end_date)

def total_expenses():
    """Calculate total expenses for all time."""
    return calculate_expenses()

def calculate_expenses(start_date=None, end_date=None):
    """Calculate total expenses within the given date range."""
    if start_date and end_date:
        expenses = AddExpense.query.filter(AddExpense.date.between(start_date, end_date)).all()
    else:
        expenses = AddExpense.query.all()
    
    return sum(int(expense.amount) for expense in expenses)
