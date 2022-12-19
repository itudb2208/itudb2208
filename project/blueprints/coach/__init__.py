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
        cursor.execute(f"""SELECT Coaches.tmID as tmID, Coaches.year as Season,Coaches.lgID as League,Teams.name as Team ,Coaches.g as Games,Coaches.w as Win,Coaches.l as Loose,Coaches.t as Tie,
        postg as Playoff_Games,postw as Playoff_Win,postl as Playoff_Loose,postt as Playoff_Tie
        FROM Coaches JOIN Teams ON (Coaches.tmID=Teams.tmID) WHERE (coachID=?) GROUP BY Coaches.year,Teams.name""", (coachID,))
        stats = cursor.fetchall()
        cursor.execute(f"""SELECT AwardsCoaches.year as Season,award as Award
        FROM Coaches JOIN AwardsCoaches ON (AwardsCoaches.year=Coaches.year)AND(AwardsCoaches.coachID=Coaches.coachID) WHERE (Coaches.coachID=?)""", (coachID,))
        awards = cursor.fetchall()
        awardWinner = len(awards) > 0
    
    return render_template('coach.html',general_headers=[("firstName","firstName"),("lastName","lastName"),("nameNick","nameNick"),("birthYear","birthYear"),("birthMon","birthMon"),
    ("birthDay","birthDay"),("birthCountry","birthCountry"),("birthCity","birthCity"),("deathYear","deathYear"),("deathMon","deathMon"),("deathDay","deathDay"),("deathCountry","deathCountry"),("deathCity","deathCity")],
    stats_headers=[("Season","Season"),("League","lgID"),("Team","tmID"),("Games","g"),("Win","w"),("Loose","l"),("Tie","t"),("Playoff_Games","postg"),("Playoff_Wins","postw"),("Playoff_Loose","postl"),("Playoff_Tie","postt")],
    awards_headers=[("Season","year"),("Award","award")],general=general,stats=stats,awards=awards,awardWinner=awardWinner, coachID=coachID)


@bp.route('/update', methods=['POST'])
def update():
    update_dict = dict(request.json)
    coach_ID = update_dict.pop("coachID")
    
    with get_db() as connection:
        cursor = connection.cursor()
        for table_name, table_updates in update_dict.items():
            for idx, table_update in table_updates.items():
                where_keys = table_update.pop("wherekeys", None)
                where_values = table_update.pop("wherevalues", [])
                where_clause = ""
                if where_keys:
                    where_keys = where_keys.split(' ')
                    where_values = where_values.split('~')
                    where_clause = f"AND {' AND '.join([key+'=?' for key in where_keys])}"

                cursor.execute(f"""UPDATE {table_name} SET {','.join([f"{key}=?" for key in table_update.keys()])} WHERE coachID=? {where_clause}""", (*table_update.values(), coach_ID, *where_values))
    return index(coach_ID)
    