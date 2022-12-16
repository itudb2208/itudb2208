import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('query', __name__, url_prefix='/')

@bp.route('/search', methods=['POST'])
def search():
    search_parameters = json.loads(request.form.get('search_parameters'))
    search_mode = request.form.get('search_mode')
    if not search_mode in ['Teams', 'Master']:
        return render_template('index.html')
        
    column_names = None
    with get_db() as connection:
        cursor = connection.cursor()
        column_names = set([row['name'] for row in cursor.execute(f"PRAGMA table_info({table_name});").fetchall()])
        
    rows = db_filter(search_mode, column_names, search_parameters)
    
    return render_template('search_results.html', headers=column_names, results=rows)
    
def db_filter(table_name, attributes, column_names=None):
    """
    table_name: str
        Which table to filter. It must be guaranteed that it is a safe string.
    attributes: dict
        Specifies which attributes will be filtered. Elements are like {'attribute': (desired_values list, bool indicating whether filter must be the exact value)}.
    Returns all rows if attribute dict is correct, None otherwise.
    column_names: set or list
        (Optional) Specifies the column names of the table.
    """
    
    with get_db() as connection:
        cursor = connection.cursor()
        
        if column_names is None:
            column_names = set([row['name'] for row in cursor.execute(f"PRAGMA table_info({table_name});").fetchall()])
            
        statement = f"SELECT * FROM {table_name} WHERE "
        where_statement = ""  # Is going to be added to 'statement'
        args = []  # Args for %s% placeholders in statement
        for key, (value, is_exact) in attributes.items():
            if key not in column_names:
                return None
        
            if is_exact:
                where_statement += f"{key} IN {('?,' * len(value))[-1]} AND"
            else:
                where_statement += f"{key} LIKE '%?%' AND"
            args.extend(value)
        statement += where_statement[:-3]
        cursor.execute(statement, (*args,))
        return cursor.fetchall()