from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('team', __name__, url_prefix='/search/tmID')

@bp.route('/<string:tmID>', methods=['GET'])
def index(tmID):
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT name,lgID,franchID FROM Teams  WHERE (tmID="{tmID}") GROUP BY name""")
        general = cursor.fetchall()
        cursor.execute(f"""SELECT year as Season, rank as Ranking,Fullname as Playoff_Degree,G as Games_Played,W as Win,L as Loose,T as Tie,Pts as Points,GF as Goals_For,GA as Goals_Against FROM Teams LEFT JOIN abbrev ON (playoff=Code) WHERE (tmID="{tmID}") GROUP BY year""")
        regular_stats = cursor.fetchall()
        cursor.execute(f"""SELECT year,G,W,L,T,GF,GA FROM TeamsPost WHERE (tmID="{tmID}") GROUP BY year""")
        post_stats = cursor.fetchall()
    return render_template('team.html',general_headers=["name"],regular_headers=["name"],post_headers=["name"],general=general,regular=regular_stats,post=post_stats)

