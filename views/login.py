import random
import string

from db import db
from main import app, conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint


login = Blueprint('login', __name__)
letters = [s for s in string.ascii_lowercase]
numbers = [str(i) for i in range(10)]


@app.route('/signin', methods=['GET', 'POST'])
def login():
    data = {"T1": {'username': request.form.get("username"), 'password': request.form.get("password")}}
    res = db.select(conn, {'': ['Account']}, {"T1": ['aid']}, data)
    if len(res) != 0:
        response = make_response(url_for('homepage'))
        response.set_cookie('aid', res[0]['aid'])
        return redirect(response)
    else:
        return render_template('SignIn.html', msg = "error user name or password")


@app.route('/tosignup', methods=['GET', 'POST'])
def to_sign_up():
    return render_template('SignUp.html')


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    data = {'username': request.form.get("username"), 'password': request.form.get("password"),
            'email': request.form.get("email")}

    aids = db.select(conn, {'': ['Account']}, {"T1": ['aid']}, dict())
    aids = set([t['aid'] for t in aids])
    data['aid'] = ''.join(random.choice(letters + numbers) for j in range(10))
    while data['aid'] in aids:
        data['aid'] = ''.join(random.choice(letters + numbers) for j in range(10))

    db.insert(conn, 'Account', data)
    response = make_response(url_for('homepage'))
    response.set_cookie('aid', data['aid'])
    return redirect(response)
