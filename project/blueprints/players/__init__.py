from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('players', __name__, url_prefix='/')

@bp.route('/players', methods=['GET'])
def index():
    return render_template('players.html')

