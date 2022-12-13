from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('about', __name__, url_prefix='/about')

@bp.route('', methods=['GET'])
def about():
    return render_template('about.html')