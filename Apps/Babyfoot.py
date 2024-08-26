from FlaskApp import *
prefix = "/Babyfoot/"
import mysql.connector
from DB_CONFIG import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, DB_babyfoot

db_config = {
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'host': MYSQL_HOST,
    'database': DB_babyfoot,
    'port': 3306,
}

def Read_Table(table_name):
    if "--github" in argv:
        return ["Erwan", "Nat", "Sol", "Alex"]
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = f"SELECT * FROM `{table_name}` LIMIT 10;"
    cursor.execute(query)
    result = cursor.fetchall()


    cursor.close()
    connection.close()
    if table_name == "Player":
        return [s for number, s in result]
    return result

def Create_Player(username):
    # Establish a connection to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    check_query = "SELECT COUNT(*) FROM Player WHERE username = %s;"
    cursor.execute(check_query, (username,))
    count = cursor.fetchone()[0]

    if count > 0:
        result = "Player with this username already exists!"
    else:
        query = "INSERT INTO Player (username) VALUES (%s);"    # Prepared statement to avoid SQL injection

        try:
        
            cursor.execute(query, (username,))    # Execute the query with the provided username
            
        
            connection.commit()    # Commit the transaction to the database
            result = "Player added successfully!"
        except mysql.connector.Error as err:
            result = f"Error: {err}"
            connection.rollback()  # Rollback in case of an error
        finally:
            # Always close the cursor and connection
            cursor.close()
            connection.close()
    return result

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
    GROUP BY m.id, m.score_team_1, m.score_team_2, m.date;
    """
    
    
    if limit is not None:   # Add the LIMIT clause if a limit is specified
        query += " LIMIT %s"

    cursor.execute(query)
    result = cursor.fetchall()


    cursor.close()
    connection.close()
    return result

def get_user_ids_from_usernames(cursor, usernames):
    if not usernames:
        return {}
    
    query = "SELECT username, id FROM Player WHERE username IN (%s)" % ','.join(['%s'] * len(usernames))
    cursor.execute(query, usernames)
    user_id_map = {username: user_id for username, user_id in cursor.fetchall()}
    
    return user_id_map

def create_match_and_players(team1_players, team2_players, score1, score2, date=None):

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        all_players = team1_players + team2_players

        team1_user_ids = get_user_ids_from_usernames(cursor, team1_players)
        team2_user_ids = get_user_ids_from_usernames(cursor, team2_players)


        # Insert into the Match table
        match_query = """
        INSERT INTO Game_Match (score_team_1, score_team_2, date, game)
        VALUES (%s, %s, %s, %s)
        """
        match_values = (score1, score2, date, 1)  # 'game' is a fixed value, 1 for babyfoot
        cursor.execute(match_query, match_values)
        match_id = cursor.lastrowid     # Get the ID of the inserted match

        # Prepare data for Match_Players
        match_players_values = [(match_id, user_id, 1) for user_id in team1_user_ids.values()] + \
                               [(match_id, user_id, 2) for user_id in team2_user_ids.values()]

        # Insert into the Match_Players table
        match_players_query = """
        INSERT INTO Match_Players (match_id, user_id, team)
        VALUES (%s, %s, %s)
        """
        cursor.executemany(match_players_query, match_players_values)

        # Commit the transaction
        connection.commit()
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        # Close the cursor and the connection
        cursor.close()
        connection.close()

def routes():
    @app.route(prefix)
    def Babyfoot():
        return render_template(prefix + "navbar.html")

    @app.route(prefix + "Players")
    def Babyfoot_Players():
        players = Read_Table("Player")
        return render_template(prefix + "Players.html", players=players)
    
    @app.route(prefix + "Insert_Player", methods=['POST'])
    def Insert_Babyfoot_Players():
        data = request.get_json()
        username = data.get('username')    # Extract the 'username' from the JSON data

        if not username:
            return jsonify({"error": "Username is required"}), 400

        result = Create_Player(username)
        return jsonify({"message": result})

    @app.route(prefix + "Add_Player")
    def Add_Babyfoot_Players():
        return render_template(prefix + "Add_Player.html")
    
    @app.route(prefix + 'matches', methods=['GET'])
    def Babyfoot_matches():
        limit = request.args.get('limit', default=None, type=int)
        match_data = Request_Matches(limit)
        return render_template(prefix + 'Matches.html', matches=match_data)   
     
    @app.route(prefix + 'test')
    def eetete():
        return render_template(prefix + 'test.html')
    
    @app.route(prefix + 'Add_Match')
    def Babyfoot_Add_Match():
        players = Read_Table("Player")
        return render_template(prefix + 'Add_Match.html', players=players)
    
    @app.route(prefix + '/dev_submit_match', methods=['POST'])
    def dev_submit_match():
        players = Read_Table("Player")
        team1_players = request.form.getlist('team1_players')[0].split(",")
        team2_players = request.form.getlist('team2_players')[0].split(",")
        team1_score = request.form.get('team1_score')
        team2_score = request.form.get('team2_score')
        match_date = request.form.get('match_date') 

        data = request.form.to_dict(flat=False)
        print("-----------------------")
        print(team1_players)
        print(team2_players)

        if all(name in players for name in team1_players) and all(name in players for name in team2_players):
            try:
                create_match_and_players(team1_players, team2_players, team1_score, team2_score,match_date)
                return "OK"
            except Exception as e:
                return e
        else:
            missing_from_team1 = [name for name in team1_players if name not in players]
            missing_from_team2 = [name for name in team2_players if name not in players]
            return {
                "missing_from_team1": missing_from_team1,
                "missing_from_team2": missing_from_team2
            }
        
        return f"{team1_players} {team1_score} {team2_players} {team2_score} {match_date}<br>{data}"