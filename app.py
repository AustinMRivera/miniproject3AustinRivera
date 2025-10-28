# INF601 - Advanced Programming in Python
# Austin Rivera
# Mini Project 3

# This is my personal finance tracker app. I built it to track income and expenses simply.
# Features: Register/login, add transactions, dashboard summary, view/delete with modal.

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key_change_later'  # I set this random for security

import os

# Get absolute path to current folder (where app.py lives)
basedir = os.path.abspath(os.path.dirname(__file__))

# Make sure the instance folder exists and is writable
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)

# Build the absolute database path
db_path = os.path.join(instance_path, 'finance_tracker.db')

# Use an absolute SQLite URI
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model - main table for accounts
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # Hashed for safety
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transactions = db.relationship('Transaction', backref='user', lazy=True)  # Link to transactions

    def set_password(self, password):
        # I used bcrypt for security because plain passwords are risky
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

# Transaction model - linked to User with foreign key
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # FK to User
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # I added categories like 'food' or 'salary'
    description = db.Column(db.String(200))
    transaction_type = db.Column(db.String(20), nullable=False)  # 'income' or 'expense'
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Decorator for protected routes
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# Home page
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# Register page with form (GET/POST)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        confirm = request.form['confirm_password']
        if password != confirm:
            flash('Passwords mismatch.', 'danger')
            return render_template('register.html')
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username/email taken.', 'danger')
            return render_template('register.html')
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registered. Log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login page with form (GET/POST)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier'].strip()
        password = request.form['password']
        user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Welcome back!', 'success')
            return redirect(url_for('dashboard'))
        flash('Bad login.', 'danger')
    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('index'))

# Dashboard page with calculations
@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    income = db.session.query(db.func.sum(Transaction.amount)).filter_by(user_id=user_id, transaction_type='income').scalar() or 0
    expense = db.session.query(db.func.sum(Transaction.amount)).filter_by(user_id=user_id, transaction_type='expense').scalar() or 0
    balance = income - expense  # Simple math for balance
    recent = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc()).limit(5).all()
    return render_template('dashboard.html', balance=balance, income=income, expense=expense, recent=recent)

# Add transaction page with form (GET/POST)
@app.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category'].strip() or 'No category'
        description = request.form['description'].strip()
        t_type = request.form['transaction_type']
        tx = Transaction(user_id=session['user_id'], amount=amount, category=category, description=description, transaction_type=t_type)
        db.session.add(tx)
        db.session.commit()
        flash(f'Added {t_type}.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_transaction.html')

# Transactions list page
@app.route('/transactions')
@login_required
def transactions():
    t_type = request.args.get('type', 'all')
    query = Transaction.query.filter_by(user_id=session['user_id'])
    if t_type != 'all':
        query = query.filter_by(transaction_type=t_type)
    txs = query.order_by(Transaction.date.desc()).all()
    return render_template('transactions.html', transactions=txs, current_filter=t_type)

# Delete transaction (POST from modal)
@app.route('/delete_transaction/<int:tx_id>', methods=['POST'])
@login_required
def delete_transaction(tx_id):
    tx = Transaction.query.get_or_404(tx_id)
    if tx.user_id != session['user_id']:
        flash('Not yours to delete.', 'danger')
        return redirect(url_for('transactions'))
    db.session.delete(tx)
    db.session.commit()
    flash('Deleted.', 'info')
    return redirect(url_for('transactions'))

# Run the app - auto create DB if not there
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables on first run, no separate command needed
    app.run(debug=True)
