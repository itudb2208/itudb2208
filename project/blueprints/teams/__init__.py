from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('teams', __name__, url_prefix='/teams')

@bp.route('', methods=['GET'])
def index():
    return render_template('teams.html')

