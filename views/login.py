import random
import string

from db.db import conn
from db import db
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint
from views.homepage import all_records, add_record, adding_record

login = Blueprint('login', __name__)
letters = [s for s in string.ascii_lowercase]
numbers = [str(i) for i in range(10)]


@login.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    data = {"T1": {'name': request.form.get("username"), 'pwd': request.form.get("password")}}
    res = db.select(conn, {'': ['Account']}, {"T1": ['aid']}, data)
    if len(res) != 0:

        resp = make_response(redirect(url_for("homepage.all_records")))
        resp.set_cookie(key = 'aid', value = res[0]['aid'], expires = None)
        return resp
    else:
        return render_template('/login/SignIn.html', msg = "error user name or password")


@login.route('/to_sign_up', methods=['GET', 'POST'])
def to_sign_up():
    return render_template('/login/SignUp.html')


@login.route('/sign_up', methods=['GET', 'POST'])
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
