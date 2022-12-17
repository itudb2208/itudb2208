from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('player', __name__, url_prefix='/search/playerID')

@bp.route('/<string:playerID>', methods=['GET'])
def index(playerID):
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT firstName,lastName,nameNick,height,weight,firstNHL,lastNHL,pos,birthYear,birthMon,birthDay,birthCountry,birthCity,deathYear,deathMon,deathDay,deathCountry,deathCity
FROM Master WHERE (playerID="{playerID}")""")
        general = cursor.fetchall()
        cursor.execute(f"""SELECT Scoring.year,Scoring.lgID,Teams.name as Team_Name,pos,GP,Scoring.G,A,Scoring.Pts,PIM,"+/-",PPG,PPA,SHG,SHA,GWG,GTG,SOG
FROM Scoring JOIN Teams ON (Scoring.tmID=Teams.tmID) WHERE (playerID="{playerID}") GROUP BY Scoring.year,Teams.name""")
        stats = cursor.fetchall()
        cursor.execute(f"""SELECT award,AwardsPlayers.year
FROM Scoring JOIN AwardsPlayers ON (AwardsPlayers.year=Scoring.year)AND(AwardsPlayers.playerID=Scoring.playerID) WHERE (Scoring.playerID="{playerID}")""")
        awards = cursor.fetchall()
    
    return render_template('player.html',general_headers=["name"],stats_headers=["name"],awards_headers=["name"],general=general,stats=stats,awards=awards)
