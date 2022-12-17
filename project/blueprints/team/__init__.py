from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('team', __name__, url_prefix='/search')

@bp.route('/<string:tmID>', methods=['GET','POST'])
def index(tmID):
    # with get_db() as connection:
    #     cursor = connection.cursor()
    #     team = cursor.execute("SELECT * FROM Teams WHERE ")
    return render_template('team.html',pl='yes',id=tmID)

