from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('coach', __name__, url_prefix='/search/coachID')

@bp.route('/<string:coachID>', methods=['GET'])
def index(coachID):
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT firstName,lastName,nameNick,birthYear,
        birthMon,birthDay,birthCountry,birthCity,deathYear,deathMon,deathDay,deathCountry,deathCity
        FROM Master WHERE (coachID=?)""", (coachID,))
        general = cursor.fetchall()
        cursor.execute(f"""SELECT Coaches.year as Season,Coaches.lgID as League,Teams.name as Team ,Coaches.g as Games,Coaches.w as Win,Coaches.l as Loose,Coaches.t as Tie,
        postg as Playoff_Games,postw as Playoff_Win,postl as Playoff_Loose,postt as Playoff_Tie
        FROM Coaches JOIN Teams ON (Coaches.tmID=Teams.tmID) WHERE (coachID=?) GROUP BY Coaches.year,Teams.name""", (coachID,))
        stats = cursor.fetchall()
        cursor.execute(f"""SELECT AwardsCoaches.year as Season,award as Award
        FROM Coaches JOIN AwardsCoaches ON (AwardsCoaches.year=Coaches.year)AND(AwardsCoaches.coachID=Coaches.coachID) WHERE (Coaches.coachID=?)""", (coachID,))
        awards = cursor.fetchall()
    
    return render_template('coach.html',general_headers=["firstName","lastName","nameNick","birthYear","birthMon",
    "birthDay","birthCountry","birthCity","deathYear","deathMon","deathDay","deathCountry","deathCity"],
    stats_headers=["Season","League","Team","Games","Win","Loose","Tie","Playoff_Games","Playoff_Wins","Playoff_Loose","Playoff_Tie"],
    awards_headers=["Season","Award"],general=general,stats=stats,awards=awards)
