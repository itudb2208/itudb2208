import sqlite3 as dbapi2
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = dbapi2.connect(
            current_app.config['DATABASE'],
            detect_types=dbapi2.PARSE_DECLTYPES
        )
        g.db.row_factory = dbapi2.Row

    return g.db

def close_db(p=None):  # Parameter p is required for built-in Flask callbacks, but is not used
    db = g.pop('db', None)

    if db is not None:
        db.close()

def register_app(app):
    app.teardown_appcontext(close_db)