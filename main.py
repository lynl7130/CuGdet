from flask import Flask, request, redirect, session, url_for, render_template
import os
from datetime import timedelta

from views.homepage import homepage
from views.login import login
from views.plans import plans
from views.stat import stat
from views.stocks import stocks


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

app.register_blueprint(homepage, url_prefix='/homepage')
app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(plans, url_prefix='/plans')
app.register_blueprint(stat, url_prefix='/stat')
app.register_blueprint(stocks, url_prefix='/stocks')


@app.route('/')
def index():
    return render_template('SignIn.html')


if __name__ == '__main__':
    app.run(debug = True, port = 8080)
