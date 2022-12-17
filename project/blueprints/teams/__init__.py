from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('teams', __name__, url_prefix='/')

@bp.route('/teams/', methods=['GET'])
def index():
    return render_template('teams.html')

