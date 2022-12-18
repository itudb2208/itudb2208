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
        cursor.execute(f"""SELECT year as Season, rank as Ranking,Fullname as Playoff_Degree,
        G as Games_Played,W as Win,L as Loose,T as Tie,Pts as Points,GF as Goals_For,GA as Goals_Against 
        FROM Teams LEFT JOIN abbrev ON (playoff=Code) WHERE (tmID=?) GROUP BY year""", (tmID,))
        regular_stats = cursor.fetchall()
        cursor.execute(f"""SELECT year as Season,G as Games_Played,W as Win,L as Loose,T as Tie,GF as Goals_For,GA as Goals_Against FROM TeamsPost WHERE (tmID=?) GROUP BY year""", (tmID,))
        post_stats = cursor.fetchall()
    return render_template('team.html',general_headers=["Name","League","Franchise"],
    regular_headers=["Season","Ranking","Playoff_Degree","Games_Played","Win","Loose","Tie","Points","Goals_For","Goals_Against"],
    post_headers=["Season","Games_Played","Win","Loose","Tie","Goals_For","Goals_Against"],
    general=general,regular=regular_stats,post=post_stats)

