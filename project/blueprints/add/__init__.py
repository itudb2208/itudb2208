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
            table_name = data.pop('table')
            types = dict([(row['name'],row['type']) for row in cursor.execute(f"PRAGMA table_info({table_name});").fetchall()])
            for k,v in data.items():
                if types[k] != "INTEGER":
                    values.append(str(v))
                else:
                    values.append(v)

            st_value = "("
            for i in range(len(values)-1):
                st_value += "?,"
            st_value += "?)"
            print(f"INSERT INTO {table_name} ({','.join(data.keys())}) VALUES {st_value}",tuple(values))
            row = cursor.execute(f"INSERT INTO {table_name} ({','.join(data.keys())}) VALUES {st_value}",tuple(values))
            if(row == None):
                print("Failed.")
            else:
                print("Succesful.")

    else:
        return render_template('add.html')

    return render_template('add.html')

@bp.route('/addTeamStat', methods=['GET','POST'])
def teampage_add():
    add()
    return redirect(url_for(f"""team.index""",tmID=request.form['tmID']))
    
@bp.route('/addPlayerStat', methods=['GET','POST'])
def playerpage_add():
    add()
    return redirect(url_for(f"""player.index""",playerID=request.form['playerID']))
    
@bp.route('/addCoachStat', methods=['GET','POST'])
def coachpage_add():
    add()
    return redirect(url_for(f"""coach.index""",coachID=request.form['coachID']))


@bp.route('/select', methods=["GET","POST"])
def select():
    if request.method == "GET":
        return redirect(url_for("add.add"))

    table_name = request.form["tables"]
    print(table_name)
    
    with get_db() as connection:
        cursor = connection.cursor()
        div_codes = False
        conf_codes = False

        if table_name == "Teams":

            divs = cursor.execute(f"SELECT * FROM abbrev WHERE Type='Division';").fetchall()
            div_codes = [div["code"] for div in divs]

            confs = cursor.execute(f"SELECT * FROM abbrev WHERE Type='Conference';").fetchall()
            conf_codes = [conf["code"] for conf in confs]


        elif table_name == "Master":
            pass

        columns = dict([(row['name'],row['type']) for row in cursor.execute(f"PRAGMA table_info({table_name});").fetchall()])
        reqs = dict([(row['name'],row['notnull']) for row in cursor.execute(f"PRAGMA table_info({table_name});").fetchall()])
        print(columns)
        print(reqs)
    return render_template('add.html',columns=columns, table_name=table_name, div_codes=div_codes,conf_codes=conf_codes, reqs=reqs)
