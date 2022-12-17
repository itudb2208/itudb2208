from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('coach', __name__, url_prefix='/search/coachID')

@bp.route('/<string:tmID>', methods=['GET'])
def index(coachID):
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT firstName,lastName,nameNick,height,weight,firstNHL,lastNHL,pos,birthYear,birthMon,birthDay,birthCountry,birthCity,deathYear,deathMon,deathDay,deathCountry,deathCity
FROM Master WHERE (playerID="{coachID}")""")
        general = cursor.fetchall()
        cursor.execute(f"""SELECT Coaches.year,Coaches.lgID,Teams.name as Team_Name,Coaches.g,Coaches.w,Coaches.l,Coaches.t,postg,postw,postl,postt
FROM Coaches JOIN Teams ON (Coaches.tmID=Teams.tmID) WHERE (coachID="{coachID}") GROUP BY Coaches.year,Teams.name")""")
        stats = cursor.fetchall()
        cursor.execute(f"""SELECT award,AwardsCoaches.year
FROM Coaches JOIN AwardsCoaches ON (AwardsCoaches.year=Coaches.year)AND(AwardsCoaches.coachID=Coaches.coachID) WHERE (Coaches.coachID="{coachID}")""")
        awards = cursor.fetchall()
    
    return render_template('coach.html',general_headers=["name"],stats_headers=["name"],awards_headers=["name"],general=general,stats=stats,awards=awards)
