### INF601 - Advanced Programming in Python
### Austin Rivera
### Mini Project 3


# Personal Finance Tracker

A simple web app to track your money - add income/expenses, see summaries, and manage everything securely.

## Description

This is my Flask app for Mini Project 3. It lets users sign up, log in, add income or expense entries with categories and notes, see a dashboard with total balance, view all entries with filters, and delete them using a popup modal. I used SQLite for the database with two tables (users and transactions) connected by a foreign key. The site has 6 pages, uses Bootstrap for looks (including the modal), and has a form that handles GET and POST. I structured the folders like tutorials but added my own touches, like category fields for realism. It's secure with hashed passwords and session-based login.

## Getting Started

### Dependencies

* Python 3.8 or higher 
* Windows 10/11 or macOS (tested on Windows)
* No extra OS stuff needed
* Install packages with:
pip install -r requirements.txt

### Installing

* Download from GitHub: Go to the repo and click "Code" > "Download ZIP", then unzip to a folder.
* No mods needed - files are ready.

### Executing program

* Open the folder in your terminal or command prompt.
* Create/activate virtual env (optional but good):
python -m venv venv
venv\Scripts\activate (on Windows)
* Install deps:
pip install -r requirements.txt
* Run the server:
python app.py
* Open browser to http://localhost:5000
* Register an account, log in, and start adding entries.

## Help

If DB doesn't create: Run python app.py - it auto-makes tables on first run.
Port busy: Change app.run(port=5001) in app.py.
Flash messages not showing: Check Bootstrap CDN in base.html is loaded.
Reset data: Delete instance/finance_tracker.db and rerun.

## Authors

Austin Rivera  
GitHub: @AustinMRivera

## Version History

* 1.0
    * Full app with auth, dashboard, forms, modal delete
* 0.2
    * Added templates and styling
* 0.1
    * Initial setup and models

## Acknowledgments

Inspired by Flask tutorials online.
Bootstrap docs for modal.
README from instructor template.
