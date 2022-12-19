import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db
from werkzeug.datastructures import MultiDict
bp = Blueprint('delete', __name__, url_prefix='/search')

@bp.route('/', methods=['POST'])
def delete():
    request.form = MultiDict(request.form) # Make the dict mutable
    ids = request.form.getlist('ids')

    which_table = request.form.pop('which_table')
    if which_table == "tmID":
        which_table = "name"

    table_name = "Teams" if which_table == "name" else "Master"

    statement = f"""DELETE FROM {table_name} WHERE"""

    last = ids.pop()

    for id in ids:
        statement += f""" ({which_table} = "{id}") OR"""
    statement += f""" ({which_table} = "{last}")"""

    print(statement)
    
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute(statement)
        cursor.fetchall()

    return redirect(url_for("home.index"))

@bp.route('/tmID/delete', methods=['POST'])
def teams():
    tmID = deleteIndividual("tmID",MultiDict(request.form))
    return redirect(url_for(f"""team.index""",tmID=tmID))

@bp.route('/playerID/delete', methods=['POST'])
def players():
    playerID = deleteIndividual("playerID",MultiDict(request.form))
    return redirect(url_for(f"""player.index""",playerID=playerID))

@bp.route('/coachID/delete', methods=['POST'])
def coaches():
    coachID = deleteIndividual("coachID",MultiDict(request.form))
    return redirect(url_for(f"""coach.index""",coachID=coachID))

def deleteIndividual(which_id_type,request):
    request.form = request # Make the dict mutable
    years = request.form.getlist('years')

    which_table = request.form.pop('which_table')
    which_id = request.form.pop('which_id')

    statement = f"""DELETE FROM {which_table} WHERE ({which_id_type} = "{which_id}") AND ("""

    last = years.pop()

    for year in years:
        statement += f""" (year = "{year}") OR"""
    statement += f""" (year = "{last}"))"""
    
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute(statement)
        cursor.fetchall()

    return which_id