from datetime import datetime
from flask import Flask, render_template, redirect, request, url_for, flash, session
from models import db, Users, AddExpense
from config import Config
from utils.expense_utils import format_currency, get_expenses_summary
from utils.users_utils import get_user_by_email_and_password, get_user_full_name


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


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


@app.route('/')
def index():
    if is_logged_in():
        user_id = session['user_id']
        user_name = get_user_full_name(user_id)
        expenses_summary = get_expenses_summary(user_id)
        expenses = {key: format_currency(value) for key, value in expenses_summary.items()}
        return render_template('index.html', expenses=expenses, user_name=user_name)
    return redirect(url_for('login'))


@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_expense = AddExpense(
            date=datetime.now().date(),
            category=request.form.get('category'),
            description=request.form.get('description'),
            amount=request.form.get('amount'),
            user_id=session['user_id']
        )
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add_expense.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        repeat_password = request.form.get('repeatPassword')

        validation_error = validate_registration_data(fname, lname, email, password, repeat_password)
        if validation_error:
            flash(validation_error, 'danger')
            return redirect(url_for('register'))

        userinfo = Users(first_name=fname, last_name=lname, email=email, password=password)
        db.session.add(userinfo)
        db.session.commit()
        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email_and_password(email=email, password=password)

        if user:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        flash('Login failed. Incorrect password. Please try again.', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out. Please login again.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
