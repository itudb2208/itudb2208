from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import get_db

bp = Blueprint('player', __name__, url_prefix='/search/playerID')

@bp.route('/<string:playerID>', methods=['GET'])
def index(playerID):
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT firstName,lastName,nameNick,HOF.year as HallOfFame_Year,height as Player_Weight,weight as Player_Height,firstNHL,lastNHL,pos as Position,birthYear,
        birthMon,birthDay,birthCountry,birthCity,deathYear,deathMon,deathDay,deathCountry,deathCity
        FROM Master LEFT JOIN HOF ON (Master.hofID = HOF.hofID) WHERE (playerID=?)""", (playerID,))
        general = cursor.fetchall()
        goalie=[]
        isGoalie = general[0]['Position'] == "G"
        if isGoalie:
                cursor.execute(f"""SELECT Goalies.year as Season,Goalies.lgID as League,Teams.name as Team,GP as Games_Played, "min" as Minute,Goalies.W,Goalies.L,"T/OL"
                ,SHO,Goalies.GA,Goalies.SA,PostGP,PostMin,postW,postL,PostT,PostENG,PostSHO,PostGA,PostSA
                FROM Goalies JOIN Teams ON (Goalies.tmID=Teams.tmID) WHERE (playerID=?) GROUP BY Goalies.year,Teams.name""", (playerID,))
                goalie = cursor.fetchall()
        cursor.execute(f"""SELECT Scoring.year as Season,Scoring.lgID as League,Teams.name as Team,pos as Position,GP as Games_Played,
        Scoring.G as Goals,A as Assists,Scoring.Pts as Points,PIM,"+/-",PPG,PPA,SHG,SHA,GWG,GTG,SOG
        FROM Scoring JOIN Teams ON (Scoring.tmID=Teams.tmID) WHERE (playerID=?) GROUP BY Scoring.year,Teams.name""", (playerID,))
        stats = cursor.fetchall()
        cursor.execute(f"""SELECT AwardsPlayers.year as Season,award as Award
        FROM Scoring JOIN AwardsPlayers ON (AwardsPlayers.year=Scoring.year)AND(AwardsPlayers.playerID=Scoring.playerID) WHERE (Scoring.playerID=?)""", (playerID,))
        awardWinner = cursor.rowcount is not None
        awards = cursor.fetchall()
        
    
    return render_template('player.html',general_headers=["firstName","lastName","nameNick","HallOfFame_Year","Player_Weight","Player_Height","firstNHL","lastNHL","Position","birthYear","birthMon",
    "birthDay","birthCountry","birthCity","deathYear","deathMon","deathDay","deathCountry","deathCity"],
    stats_headers=["Season","League","Team","Position","Games_Played","Goals","Assists","Points","PIM","+/-","PPG","PPA","SHG","SHA","GWG","GTG","SOG"],
    goalie_headers=["Season","League","Team","Games_Played","Minute","W","L","T/OL","SHO","GA","SA","PostGP","PostMin","postW","postL","PostT","PostENG","PostSHO","PostGA","PostSA"],
    awards_headers=["Season","Award"],general=general,stats=stats,awards=awards,goalie=goalie,isGoalie=isGoalie,awardWinner=awardWinner)
