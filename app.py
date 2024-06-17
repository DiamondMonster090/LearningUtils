from functools import wraps
from datetime import date
from flask import Flask, render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
import google.generativeai as genai
import os
from flask_session import Session
import sqlite3

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
con = sqlite3.connect('database.db', check_same_thread=False)
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
        print(request.form.get('username'))
        print(request.form.get('password'))
        names = cur.execute('SELECT * FROM users WHERE name = ? AND password = ?', (request.form.get('username'), request.form.get('password'))).fetchall()
        thing = cur.execute('SELECT * FROM users WHERE name = ?', (request.form.get('username'),)).fetchall()
        print(names)
        print(thing)
        if len(names) == 1:
            session['user_id'] = names[0][2]
            return redirect('/')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        cur.execute('INSERT INTO users (name, password) VALUES (?, ?)', (request.form.get('username'),))
        con.commit()
        return redirect('/')
    else:
        return render_template('signup.html')
@app.route('/classes')
def classes():
    return render_template('classes.html', classes=cur.execute('SELECT * FROM classes WHERE user_id = ?', (session['user_id'],)).fetchall())

def apology(error, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", error_code=code, error_description=error)