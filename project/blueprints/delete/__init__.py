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

    table_name = "Teams" if which_table == "tmID" else "Master"

    statement = f"""DELETE FROM {table_name} WHERE"""

    last = ids.pop()

    for id in ids:
        statement += f""" ({which_table} = "{id}") OR"""
    statement += f""" ({which_table} = "{last}")"""
    
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute(statement)
        cursor.fetchall()

    return redirect(url_for("home.index"))