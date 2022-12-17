from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('team', __name__, url_prefix='/search/tmID')

@bp.route('/<string:tmID>', methods=['GET'])
def index(tmID):
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT name FROM Teams WHERE (tmID="{tmID}") GROUP BY name""")
        general = cursor.fetchall()
    return render_template('team.html',headers=["name","lgID","confID","divID"],general=general)

