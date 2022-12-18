from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

NON_EXACT_COLUMNS = set(["year", "tmID", "lgID", "franchID"])

bp = Blueprint('add', __name__, url_prefix='/add')

@bp.route('/', methods=['GET','POST'])
def add():
    if request.method == "POST":
        data = request.form.to_dict()
        print(data)
        with get_db() as connection:
            cursor = connection.cursor()
            values = list()
            table_name = data['table']
            types = dict([(row['name'],row['type']) for row in cursor.execute(f"PRAGMA table_info({table_name});").fetchall()])
            for k,v in data.items():
                if k != 'table':
                    if types[k] != "INTEGER":
                        values.append(str(v))
                    else:
                        values.append(v)

            print(f"INSERT INTO Teams VALUES {values}")
            st_value = "("
            for i in range(len(values)-1):
                st_value += "?,"
            st_value += "?)"
            print(st_value)
            row = cursor.execute(f"INSERT INTO {table_name} VALUES {st_value}",tuple(values))
            if(row == None):
                print("Failed.")
            else:
                print("Succesful.")
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
        reqs = dict([(row['name'],row['notnull']) for row in cursor.execute(f"PRAGMA table_info({table_name});").fetchall()])
        print(columns)
        print(reqs)
    return render_template('add.html',columns=columns, table_name=table_name, div_codes=div_codes,conf_codes=conf_codes, reqs=reqs)