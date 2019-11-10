from db import db
from main import conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint


stocks = Blueprint('stocks', __name__)


@stocks.route('/stock_market', methods=['GET', 'POST'])
def stock_market():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect("signin")
    all_stocks = db.select(conn, {"": ['stocks']}, {"T1": ['*']}, dict(), special = "LIMIT 100")
    return render_template("StockMarket.html", all_stocks = all_stocks)


@stocks.route('/rec_stock', methods=['GET', 'POST'])
def rec_stock():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect("signin")
    rec_stocks = db.select(conn, {"INNER JOIN": ['rec_stk', 'stocks']}, "*", {'T1': {'aid': aid}})
    return render_template("RecStock.html", rec_stocks = rec_stocks)


@stocks.route('/own_stock', methods=['GET', 'POST'])
def own_stock():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect("signin")
    own_stocks = db.select(conn, {"INNER JOIN": ['own_stk', 'stocks']}, "*", {'T1': {'aid': aid}})
    return render_template("OwnStock.html", own_stocks = own_stocks)


@stocks.route('/buy_stock', methods=['GET', 'POST'])
def buy_stock():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect("signin")
    data = {'aid': aid, 'sid': request.form.get('sid'), 'num': request.form.get('num'),
            'price': request.form.get('price')}
    db.insert(conn, 'own_stk', data)
    return redirect("own_stock")


@stocks.route('/sell_stock', methods=['GET', 'POST'])
def sell_stock():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect("signin")
    db.delete(conn, 'own_stk', {'aid': aid, 'sid': request.form.get('sid')})
    return redirect('own_stock')
