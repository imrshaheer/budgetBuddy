from datetime import datetime, timedelta
from models.AddExpenseModel import AddExpense


def get_expenses_summary():
    return {
        'today_expenses': expenses_today(),
        'yesterday_expenses': expenses_yesterday(),
        'last_7_days_expenses': expenses_last_7_days(),
        'current_month_expenses': expenses_current_month(),
        'one_year_expenses': expenses_last_year(),
        'total_expenses': total_expenses()
    }


def format_currency(amount):
        return 'PKR {:,.1f}'.format(amount)

def expenses_today():
    today = datetime.now().date()
    # Fetch expenses for today from the database
    expenses_today = AddExpense.query.filter(AddExpense.date == today).all()

    # Calculate the total amount of today's expenses
    total_amount = sum(int(expense.amount) for expense in expenses_today)

    return total_amount


def expenses_yesterday():
    # Calculate yesterday's date
    yesterday = datetime.now().date() - timedelta(days=1)
    # Query the database for expenses with yesterday's date
    expenses = AddExpense.query.filter_by(date=yesterday).all()
    # Calculate the total amount of yesterday's expenses
    total_amount = sum(int(expense.amount) for expense in expenses)

    return total_amount


def expenses_last_7_days():
    # Calculate the date 7 days ago from today
    start_date = datetime.now().date() - timedelta(days=7)
    end_date = datetime.now().date()

    # Query the database for expenses from the last 7 days
    expenses = AddExpense.query.filter(AddExpense.date.between(start_date, end_date)).all()

    # Calculate the total amount of the last 7 days' expenses
    total_amount = sum(int(expense.amount) for expense in expenses)

    return total_amount


def expenses_current_month():
    # Calculate the date 30 days ago from today
    # start_date = datetime.now().date() - timedelta(days=30)
    # end_date = datetime.now().date()

    # Get the current date
    end_date = datetime.now().date()
    # Get the start of the current month
    start_date = end_date.replace(day=1)

    # Query the database for expenses from this month days
    expenses = AddExpense.query.filter(AddExpense.date.between(start_date, end_date)).all()

    # Calculate the total amount of the last 7 days' expenses
    total_amount = sum(int(expense.amount) for expense in expenses)

    return total_amount


def expenses_last_year():
    # Get the current year
    current_year = datetime.now().year
    # Calculate the start and end dates for the current year
    start_date = datetime(current_year, 1, 1).date()
    end_date = datetime(current_year + 1, 1, 1).date()
    # Query the database for expenses from the start of the year to today
    expenses = AddExpense.query.filter(AddExpense.date.between(start_date, end_date)).all()
    # Calculate the total amount of the year's expenses
    total_amount = sum(int(expense.amount) for expense in expenses)

    return total_amount


def total_expenses():
    # Query the database for all expenses
    expenses = AddExpense.query.all()

    # Calculate the total amount of all expenses
    total_amount = sum(int(expense.amount) for expense in expenses)

    return total_amount