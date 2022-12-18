import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('team', __name__, url_prefix='/search/tmID')

@bp.route('/<string:tmID>', methods=['GET'])
def index(tmID):
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT name as Name,lgID as League,franchID as Franchise FROM Teams  WHERE (tmID=?) GROUP BY name""", (tmID,))
        general = cursor.fetchall()
        cursor.execute(f"""SELECT year as Season, rank as Ranking,Fullname as Playoff_Degree, playoff,
        G as Games_Played,W as Win,L as Loose,T as Tie,Pts as Points,GF as Goals_For,GA as Goals_Against 
        FROM Teams LEFT JOIN abbrev ON (playoff=Code) WHERE (tmID=?) GROUP BY year""", (tmID,))
        regular_stats = cursor.fetchall()
        cursor.execute(f"""SELECT year as Season,G as Games_Played,W as Win,L as Loose,T as Tie,GF as Goals_For,GA as Goals_Against FROM TeamsPost WHERE (tmID=?) GROUP BY year""", (tmID,))
        post_stats = cursor.fetchall()
    return render_template('team.html', tmID=tmID, general_headers=[("Name", "name"), ("League", "lgID"), ("Franchise", "franchID")],
    regular_headers=[("Season", "year"), ("Ranking", "rank"), ("Playoff_Degree", "playoff"), ("Games_Played", "G"), ("Win", "W"), ("Loose", "L"), ("Tie", "T"), ("Points", "Pts"), ("Goals_For", "GF"), ("Goals_Against", "GA")],
    post_headers=[("Season", "year"), ("Games_Played", "G"), ("Win", "W"), ("Loose", "L"), ("Tie", "T"), ("Goals_For", "GF"), ("Goals_Against", "GA")],
    general=general,regular=regular_stats,post=post_stats)
    
@bp.route('/update', methods=['POST'])
def update():
    update_dict = dict(request.json)
    tm_ID = update_dict.pop("tmID")
    with get_db() as connection:
        cursor = connection.cursor()
        for table_names, table_updates in update_dict.items():
            cursor.execute(f"""UPDATE {table_names} SET {','.join([f"{key}=?" for key in table_updates.keys()])} WHERE tmID=?""", (*table_updates.values(), tm_ID))
    return index(tm_ID)