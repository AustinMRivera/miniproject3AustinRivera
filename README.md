### INF601 - Advanced Programming in Python
### Austin Rivera
### Mini Project 3


# Personal Finance Tracker

A secure Flask web app for tracking income and expenses with user authentication, a responsive dashboard, and Bootstrap-powered UI.

---

## Description

This **Mini Project 3** is a fully functional personal finance tracker built with **Flask**, **SQLAlchemy**, **SQLite**, and **Bootstrap 5**.

Key features:
- Secure user registration and login (passwords hashed with `bcrypt`)
- Add income or expense transactions (amount, category, description)
- Dashboard showing total income, expenses, and **current balance**
- View all transactions with **filtering** (income/expense/all)
- **Delete transactions** using a **Bootstrap modal**
- Two-table SQLite database (`User` ↔ `Transaction`) with **foreign key**
- **5+ pages** with **template inheritance**
- **GET/POST form** handling
- **Proper folder structure** and **requirements.txt**

---

## Getting Started

### Dependencies

- **Python 3.9+**
- **Flask**
- **Flask-SQLAlchemy**
- **bcrypt**
- **Bootstrap 5** (via CDN)

> Works on Windows, macOS, Linux

**Install packages:**
```bash
pip install -r requirements.txt
