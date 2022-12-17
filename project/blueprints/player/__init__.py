from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('player', __name__, url_prefix='/search/playerID')

@bp.route('/<string:tmID>', methods=['GET'])
def index(playerID):
    # with get_db() as connection:
    #     cursor = connection.cursor()
    #     team = cursor.execute("SELECT * FROM Teams WHERE ")
    return render_template('player.html',pl='yes',id=playerID)
