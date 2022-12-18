from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('player', __name__, url_prefix='/search/playerID')

@bp.route('/<string:playerID>', methods=['GET'])
def index(playerID):
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT firstName,lastName,nameNick,Master.hofID,HOF.year as HallOfFame_Year,height as Player_Weight,weight as Player_Height,firstNHL,lastNHL,pos as Position,birthYear,
        birthMon,birthDay,birthCountry,birthCity,deathYear,deathMon,deathDay,deathCountry,deathCity
        FROM Master LEFT JOIN HOF ON (Master.hofID = HOF.hofID) WHERE (playerID=?)""", (playerID,))
        general = cursor.fetchall()
        goalie=[]
        isGoalie = general[0]['Position'] == "G"
        if isGoalie:
                cursor.execute(f"""SELECT Teams.tmID as tmID, Goalies.year as Season,Goalies.lgID as League,Teams.name as Team,GP as Games_Played, "min" as Minute,Goalies.W,Goalies.L,"T/OL"
                ,SHO,Goalies.GA,Goalies.SA,PostGP,PostMin,postW,postL,PostT,PostENG,PostSHO,PostGA,PostSA
                FROM Goalies JOIN Teams ON (Goalies.tmID=Teams.tmID) WHERE (playerID=?) GROUP BY Goalies.year,Teams.name""", (playerID,))
                goalie = cursor.fetchall()
        cursor.execute(f"""SELECT Teams.tmID as tmID, Scoring.year as Season,Scoring.lgID as League,Teams.name as Team,pos as Position,GP as Games_Played,
        Scoring.G as Goals,A as Assists,Scoring.Pts as Points,PIM,"+/-",PPG,PPA,SHG,SHA,GWG,GTG,SOG
        FROM Scoring JOIN Teams ON (Scoring.tmID=Teams.tmID) WHERE (playerID=?) GROUP BY Scoring.year,Teams.name""", (playerID,))
        stats = cursor.fetchall()
        cursor.execute(f"""SELECT AwardsPlayers.year as Season,award as Award
        FROM Scoring JOIN AwardsPlayers ON (AwardsPlayers.year=Scoring.year)AND(AwardsPlayers.playerID=Scoring.playerID) WHERE (Scoring.playerID=?)""", (playerID,))
        awardWinner = cursor.rowcount is not None
        awards = cursor.fetchall()
        
    
    return render_template('player.html',general_headers=[("firstName", "firstName"), ("lastName", "lastName"), ("nameNick", "nameNick"), ("HallOfFame_Year", "hofID"), ("Player_Weight", "height"), ("Player_Height", "weight"), ("firstNHL", "firstNHL"), ("lastNHL", "lastNHL"), ("Position", "pos"), ("birthYear", "birthYear"), ("birthMon", "birthMon"),
    ("birthDay", "birthDay"), ("birthCountry", "birthCountry"), ("birthCity", "birthCity"), ("deathYear", "deathYear"), ("deathMon", "deathMon"), ("deathDay", "deathDay"), ("deathCountry", "deathCountry"), ("deathCity", "deathCity")],
    stats_headers=[("Season", "year"), ("League", "lgID"), ("Team", "tmID"), ("Position", "pos"), ("Games_Played", "GP"), ("Goals", "G"), ("Assists", "A"), ("Points", "Pts"), ("PIM", "PIM"), ("+/-", "+/-"), ("PPG", "PPG"), ("PPA", "PPA"), ("SHG", "SHG"), ("SHA", "SHA"), ("GWG", "GWG"), ("GTG", "GTG"), ("SOG","SOG")],
    goalie_headers=[("Season", "year"), ("League", "lgID"), ("Team", "tmID"),("Games_Played", "GP"),("Minute", "min"),("W", "W"),("L","L"),("T/OL","T/OL"),("SHO","SHO"),("GA","GA"),("SA","SA"),("PostGP","PostGP"),("PostMin","PostMin"),("postW","postW"),("postL","postL"),("PostT","PostT"),("PostENG","PostENG"),("PostSHO","PostSHO"),("PostGA","PostGA"),("PostSA","PostSA")],
    awards_headers=[("Season","year"),("Award","award")],general=general,stats=stats,awards=awards,goalie=goalie,isGoalie=isGoalie,awardWinner=awardWinner, playerID=playerID)
    
    
@bp.route('/update', methods=['POST'])
def update():
    update_dict = dict(request.json)
    player_ID = update_dict.pop("playerID")
    
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

                cursor.execute(f"""UPDATE {table_name} SET {','.join([f"{key}=?" for key in table_update.keys()])} WHERE playerID=? {where_clause}""", (*table_update.values(), player_ID, *where_values))
    return index(player_ID)