from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

NON_EXACT_COLUMNS = set(["year", "tmID", "lgID", "franchID"])

bp = Blueprint('add', __name__, url_prefix='/add')

@bp.route('/', methods=['GET','POST'])
def add():
    if request.method == "POST":
        print("hello")
    else:
        return render_template('add.html')

    return render_template('add.html')

@bp.route('/select', methods=["POST"])
def select():
    table_name = request.form["tables"]
    print(table_name)
    
    with get_db() as connection:
        cursor = connection.cursor()
        if(table_name == "Teams"):
            divs = cursor.execute(f"SELECT * FROM abbrev WHERE Type='Division';").fetchall()
            div_codes = [div["code"] for div in divs]

            confs = cursor.execute(f"SELECT * FROM abbrev WHERE Type='Conference';").fetchall()
            conf_codes = [conf["code"] for conf in confs]

        columns = dict([(row['name'],row['type']) for row in cursor.execute(f"PRAGMA table_info({table_name});").fetchall()])
        print(columns)

    return render_template('add.html',columns=columns, table_name=table_name, div_codes=div_codes,conf_codes=conf_codes)