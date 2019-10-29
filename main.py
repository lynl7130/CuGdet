from flask import Flask, request, redirect, session, url_for, render_template
import os
from datetime import timedelta


from db import db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
conn, cur = db.connect(name = "proj1part2", usr = "yl4323", host = "35.243.220.243", pwd = "2262")


@app.route('/')
def index():
    return render_template('SignIn.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    res = db.select(cur, "account", "name = %s" % username)
    if len(res) == 1 and res[0][3] == password:
        return render_template('HomePage.html', username = username)


@app.route('/tosignup', methods=['GET', 'POST'])
def to_sign_up():
    return render_template('SignUp.html')


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    username = request.form.get("username")
    print(username)
    password = request.form.get("password")
    print(password)
    email = request.form.get("email")
    print(email)
    return render_template('HomePage.html', username = username, password = password)


if __name__ == '__main__':
    app.run(debug = True, port = 8080)
