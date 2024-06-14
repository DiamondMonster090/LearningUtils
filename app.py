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
@app.route('/')
def index():

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        names = cur.execute('SELECT password FROM users WHERE username = ?', request.form.get(['username'])).fetchall()
        if check_password_hash(names[0]["password"], request.form.get(['password'])):
            session['username'] = names[0]["username"]
            return redirect('/')
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return redirect('/')
    else:
        return render_template('signup.html')