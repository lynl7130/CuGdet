from flask import Flask, request, redirect, session, url_for, render_template
import os
from datetime import timedelta


from db import db
from model import *
from model.Account import Account
from model.BaseEntity import BaseEntity

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
conn = db.connect(name = "proj1part2", usr = "yl4323", host = "35.243.220.243", pwd = "2262")


@app.route('/')
def index():
    return render_template('SignIn.html')


@app.route('/signin', methods=['GET', 'POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    res = Account.select(conn, "name = '%s'" % username)
    print(res)
    if len(res) == 1 and res[0]['pwd'] == password:
        return render_template('HomePage.html', username = username)
    else:
        return render_template('SignIn.html', msg = "error user name or password")


@app.route('/tosignup', methods=['GET', 'POST'])
def to_sign_up():
    return render_template('SignUp.html')


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    Account.insert(conn, {})
    return render_template('HomePage.html', username = username, password = password)


if __name__ == '__main__':
    app.run(debug = True, port = 8080)
