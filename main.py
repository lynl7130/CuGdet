from flask import Flask, request, redirect, session, url_for, render_template
import os
from datetime import timedelta


from db import db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
conn = db.connect(name = "proj1part2", usr = "yl4323", host = "35.243.220.243", pwd = "2262")


@app.route('/')
def index():
    return render_template('SignIn.html')


if __name__ == '__main__':
    app.run(debug = True, port = 8080)
