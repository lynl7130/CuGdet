import random
import string

from db import db
from main import app, conn
from flask import request, redirect, session, url_for, render_template, make_response


letters = [s for s in string.ascii_lowercase]
numbers = [str(i) for i in range(10)]


@app.route('/own_plans', methods=['GET', 'POST'])
def own_plans():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect("signin")
    plans = db.select(conn, {"": ['plans']}, "*", {"T1": {'aid': aid}})
    return render_template("OwnPlans", plans = plans)


@app.route('/adding_plans', methods=['GET', 'POST'])
def adding_plans():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect("signin")
    return render_template("AddingPlan.html")


@app.route('/add_plans', methods=['GET', 'POST'])
def add_plans():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect("signin")
    plan = {'aid': aid, 'starting': request.form.get("starting"), 'ending': request.form.get("ending"),
            'cycle': request.form.get("cycle"), 'credit': request.form.get("credit"),
            'budget': request.form.get("budget")}

    pids = db.select(conn, {"": ['plans']}, {"T1": ['pid']}, dict())
    pids = set([t['pid'] for t in pids])
    plan['pid'] = ''.join(random.choice(letters+numbers) for j in range(10))
    while plan['pid'] in pids:
        plan['pid'] = ''.join(random.choice(letters+numbers) for j in range(10))
    db.insert(conn, 'plans', plan)
    return redirect("own_plans")


@app.route('/delete_plans', methods=['GET', 'POST'])
def delete_plans():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect("signin")
    db.delete(conn, 'plans', {'pid': request.form.get('pid')})
    return redirect("own_plans")
