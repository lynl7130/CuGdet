from db import db
from db.db import conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint


stocks = Blueprint('stocks', __name__)


def get_current_price(sids):
    sql = """select * from stock_history t1, (select MAX(time) as time, sid from stock_history group by sid having ) t2 where 
    t1.sid = t2.sid AND t1.time = t2.time;"""


@stocks.route('/stock_market', methods=['GET', 'POST'])
def stock_market():
    try:
        aid = session['aid']
    except:
        return redirect(url_for("login.sign_in"))
    all_stocks = db.select(conn, {"INNER JOIN": ['stocks_history', 'stocks']}, {"T1": ['*']}, dict(), special = "LIMIT 100")
    return render_template("/stocks/StockMarket.html", all_stocks = all_stocks)


@stocks.route('/rec_stock', methods=['GET', 'POST'])
def rec_stock():
    try:
        aid = session['aid']
    except:
        return redirect(url_for("login.sign_in"))
    rec_stocks = db.select(conn, {"INNER JOIN": ['rec_stk', 'stocks']}, "*", {'T1': {'aid': aid}})
    return render_template("/stocks/RecStock.html", rec_stocks = rec_stocks)


@stocks.route('/own_stock', methods=['GET', 'POST'])
def own_stock():
    try:
        aid = session['aid']
    except:
        return redirect(url_for("login.sign_in"))
    own_stocks = db.select(conn, {"INNER JOIN": ['own_stk', 'stocks']}, "*", {'T1': {'aid': aid}})
    return render_template("/stocks/OwnStock.html", own_stocks = own_stocks)


@stocks.route('/buy_stock', methods=['GET', 'POST'])
def buy_stock():
    try:
        aid = session['aid']
    except:
        return redirect(url_for("login.sign_in"))
    data = {'aid': aid, 'sid': request.form.get('sid'), 'num': request.form.get('num'),
            'price': request.form.get('price')}
    tmp = db.select(conn, {"INNER JOIN": ['own_stk', 'stocks']}, "*", {'T1': {'sid': data['sid'], 'aid': aid}})
    if len(tmp) == 0:
        db.insert(conn, 'own_stk', data)
    else:
        new_num = tmp[0]['num'] + data['num']
        new_price = (tmp[0]['price'] * tmp[0]['num'] + data['num'] * data['price']) / new_num
        db.update(conn, 'own_stk', {'price': new_price, 'num': new_num}, {'T1': {'sid': data['sid'], 'aid': aid}})
    return redirect(url_for(".own_stk"))


@stocks.route('/sell_stock', methods=['GET', 'POST'])
def sell_stock():
    try:
        aid = session['aid']
    except:
        return redirect(url_for("login.sign_in"))
    sid = request.form.get('sid')
    tmp = db.select(conn, {"INNER JOIN": ['own_stk', 'stocks']}, "*", {'T1': {'sid': sid, 'aid': aid}})
    cur_price = request.form.get('price')
    num = request.form.get('num')
    if tmp[0]['num'] <= num:
        db.delete(conn, 'own_stk', {'aid': aid, 'sid': request.form.get('sid')})
    else:
        new_num = tmp[0]['num'] - num
        new_price = tmp[0]['price'] * tmp[0]['num'] - cur_price * num / new_num
        db.update(conn, 'own_stk', {"=": {'price': new_price, 'num': new_num}}, {'T1': {'sid': sid, 'aid': aid}})
    return redirect(url_for(".own_stk"))
