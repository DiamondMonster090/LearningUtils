from flask import Flask, render_template, request, redirect
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
        names = cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (request.form.get(['username']), request.form.get(['password']))).fetchall()
        if len(names) == 1:

            return redirect('/')
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return redirect('/')
    else:
        return render_template('signup.html')