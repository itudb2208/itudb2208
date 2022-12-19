import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

NON_EXACT_COLUMNS = set(["firstName", "lastName", "nameNick", "name"])
TABLE_NAMES = {"Teams": "Teams", "Players": "Master", "Coaches": "Master"}
TABLE_IDS = {"Teams": "tmID", "Players": "playerID", "Coaches": "coachID"}
HEADERS_FOR_TABLES = {"Master": ["firstName", "lastName", "nameNick", "pos"],
                      "Teams": ["name"]}
ROWS_PER_PAGE = 50

bp = Blueprint('query', __name__, url_prefix='/')

@bp.route('/search', methods=['POST'])
def search():
    request.form = dict(request.form)  # Make the dict mutable
    
    search_mode = request.form.pop('search_mode')
    page_no = int(request.form.pop('pageNo'))
    
    search_attributes = {key: ([value], key not in NON_EXACT_COLUMNS, True) for key, value in request.form.items() if value != ""}
    
    table_id = TABLE_IDS.get(search_mode, None)
    table_name = TABLE_NAMES.get(search_mode, None)
    if not table_name:
        return render_template('index.html')
    
    HEADERS_FOR_TABLES[table_name].append(table_id)
           
    group_by_columns = None
    if table_name == "Teams":
        search_attributes["tmID"] = ([''], True, False)
        group_by_columns = ["name"]
    else:
        if search_mode == "Players":
            search_attributes["playerID"] = ([''], True, False)
        elif search_mode == "Coaches":
            search_attributes["coachID"] = ([''], True, False)
    rows = db_filter(table_name, search_attributes, select_columns=HEADERS_FOR_TABLES[table_name], group_by_columns=group_by_columns)
    
    page_count = ((len(rows)-1)//50)+1
    rows = rows[(page_no-1)*50:page_no*50]
    
    HEADERS_FOR_TABLES[table_name].pop()

    return render_template('search_results.html', headers=HEADERS_FOR_TABLES[table_name], results=rows,table_id=table_id, page_count=page_count, page_no=page_no, sent_form={**request.form, "search_mode": search_mode}, rows_per_page=ROWS_PER_PAGE)
    
def db_filter(table_name, attributes, select_columns=["*"], group_by_columns=None):
    """
    table_name: str
        Which table to filter. It must be guaranteed that it is a safe string.
    attributes: dict
        Specifies which attributes will be filtered. Elements are like {'attribute': (desired_values list, bool indicating whether filter must be the exact value, bool indicating equality or not equality)}.
    select_columns: set or list
        (Optional) Specifies the column names for selection.
    group_by_columns: set or list
        (Optional) Specifies the columns to use in grouping, None if not desired.
    Returns all rows if attribute dict is correct, None otherwise.
    """
    
    with get_db() as connection:
        cursor = connection.cursor()
        
        column_names = set([row['name'] for row in cursor.execute(f"PRAGMA table_info({table_name});").fetchall()])
            
        statement = f"SELECT {','.join(select_columns)} FROM {table_name} WHERE "
        where_statement = ""  # Is going to be added to 'statement'
        args = []  # Args for %s% placeholders in statement
        for key, (value, is_exact, equals) in attributes.items():
            if key not in column_names:
                return None
        
            if is_exact:
                where_statement += f"{key} {'' if equals else 'NOT'} IN ({('?,' * len(value))[:-1]}) AND "
            else:
                where_statement += f"{key} LIKE '%' || ? || '%' AND "
            args.extend(value)
        statement += where_statement[:-4]
        if group_by_columns is not None:
            statement += f" GROUP BY {','.join(group_by_columns)}"
        cursor.execute(statement, (*args,))
        return cursor.fetchall()
        