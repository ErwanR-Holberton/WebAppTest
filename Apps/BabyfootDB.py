from FlaskApp import *
prefix = "/BabyfootDB/"
from datetime import datetime
import mysql.connector
from DB_CONFIG import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, DB_babyfoot

db_config = {
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'host': MYSQL_HOST,
    'database': DB_babyfoot,
    'port': 3306,
}

def Request_Matches(limit):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = """
    SELECT
        m.id AS match_id,
        m.score_team_1,
        m.score_team_2,
        m.date AS match_date,
        GROUP_CONCAT(CASE WHEN mp.team = 1 THEN p.username ELSE NULL END) AS team1_players,
        GROUP_CONCAT(CASE WHEN mp.team = 2 THEN p.username ELSE NULL END) AS team2_players 
    FROM Game_Match m 
    JOIN Match_Players mp ON m.id = mp.match_id 
    JOIN Player p ON mp.user_id = p.id 
    WHERE m.game = 1
    GROUP BY m.id, m.score_team_1, m.score_team_2, m.date;
    ORDER BY m.date DESC;
    """
    
    
    if limit is not None:   # Add the LIMIT clause if a limit is specified
        query += " LIMIT %s"

    cursor.execute(query)
    result = cursor.fetchall()


    cursor.close()
    connection.close()
    return result


def routes():
    @app.route(prefix)
    def BabyfootDB():
        return "Nothing here"

    @app.route(prefix + "Matches")
    def BabyfootDB_Matches():
        return jsonify(Request_Matches(None))