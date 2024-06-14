from functools import wraps

from flask import Flask, render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash

from flask_session import Session
import sqlite3
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
con = sqlite3.connect('database.db')
cur = con.cursor()
def login_required(f):
    """
    Decorate routes to require login.
    Copied from CS50 week 9, finance project, from helpers.py
    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
@app.route('/')
def index():

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        names = cur.execute('SELECT password FROM users WHERE username = ?', request.form.get(['username'])).fetchall()
        if check_password_hash(names[0]["password"], request.form.get(['password'])):
            session['user_id'] = names[0]["id"]
            return redirect('/')
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (request.form.get(['username']), generate_password_hash(request.form.get(['password']))))
        con.commit()
        session['user_id'] = request.form.get(['id'])
        return redirect('/')
    else:
        return render_template('signup.html')

MAX_GEMINI_FLASH_API_CALLS = 50

def check_api(call_count, last_use_date, current_date):
    if last_use_date != current_date:
        call_count = 0
    if call_count < MAX_GEMINI_FLASH_API_CALLS:
        return True
    else:
        return False