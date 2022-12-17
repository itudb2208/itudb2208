from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('coach', __name__, url_prefix='/search/coachID')

@bp.route('/<string:tmID>', methods=['GET'])
def index(coachID):
    # with get_db() as connection:
    #     cursor = connection.cursor()
    #     team = cursor.execute("SELECT * FROM Teams WHERE ")
    return render_template('coach.html',pl='yes',id=coachID)

