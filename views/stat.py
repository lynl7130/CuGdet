from db import db
from db.db import conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint


stat = Blueprint('stat', __name__)


@stat.route('/stat', methods=['GET', 'POST'])
def statistic():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect("signin")
    