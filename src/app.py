from datetime import datetime
from flask import Flask
from flask import render_template, redirect
from flask import request, url_for, flash, session
from models.AddExpenseModel import db, AddExpense
from config import Config
from utils.expense_utils import format_currency, get_expenses_summary

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.route('/')
def index():
    expenses_summary = get_expenses_summary()
    expenses = {key: format_currency(value) for key, value in expenses_summary.items()}
    return render_template('index.html', expenses=expenses)


@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        new_expense = AddExpense(
            date=datetime.now().date(),
            category=request.form.get('category'),
            description=request.form.get('description'),
            amount=request.form.get('amount')
        )
        db.session.add(new_expense)
        db.session.commit()
        return redirect('/')
    return render_template('add_expense.html')


if __name__ == '__main__':
    app.run(debug=True)
