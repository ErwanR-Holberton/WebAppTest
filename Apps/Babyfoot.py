from FlaskApp import *
prefix = "/Babyfoot/"
from datetime import datetime
import mysql.connector, requests
from DB_CONFIG import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, DB_babyfoot

db_config = {
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'host': MYSQL_HOST,
    'database': DB_babyfoot,
    'port': 3306,
}

def Read_Table(table_name):
    if LOCAL_MODE:
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
    if "--github" in argv or "--local" in argv:
        try:
            return requests.get(SERVER_ADDRESS + "/BabyfootDB/Matches").json()
        except (requests.RequestException, ValueError) as e:
            print(e)
            return None
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
        if date:    # Query with date
            match_query = """
            INSERT INTO Game_Match (score_team_1, score_team_2, date, game)
            VALUES (%s, %s, %s, %s)
            """
            match_values = (score1, score2, date, 1)
        else:       # Query without date
            match_query = """
            INSERT INTO Game_Match (score_team_1, score_team_2, game)
            VALUES (%s, %s, %s)
            """
            match_values = (score1, score2, 1)

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

def get_rankings():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = """
    WITH Match_Winners AS (
    SELECT 
        GM.id AS match_id,
        CASE 
            WHEN GM.score_team_1 > GM.score_team_2 THEN 1
            WHEN GM.score_team_2 > GM.score_team_1 THEN 2
            ELSE 0  -- For a draw
        END AS winning_team
    FROM Game_Match GM
    ),
    Player_Wins AS (
        SELECT 
            P.id AS player_id,
            P.username,
            COUNT(MP.match_id) AS wins
        FROM Player P
        JOIN Match_Players MP ON P.id = MP.user_id
        JOIN Match_Winners MW ON MP.match_id = MW.match_id
        WHERE MP.team = MW.winning_team
        GROUP BY P.id, P.username
    ),
    Player_Total_Matches AS (
        SELECT 
            P.id AS player_id,
            COUNT(MP.match_id) AS total_matches
        FROM Player P
        JOIN Match_Players MP ON P.id = MP.user_id
        GROUP BY P.id
    )
    SELECT 
        PW.player_id,
        PW.username,
        PW.wins,
        PTM.total_matches,
        (PW.wins / PTM.total_matches) * 100 AS win_percentage
    FROM Player_Wins PW
    JOIN Player_Total_Matches PTM ON PW.player_id = PTM.player_id
    ORDER BY win_percentage DESC, PW.wins DESC;
    """

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()
    return result

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
        match_data.sort(key=lambda x: x[3], reverse=True)
        players = Read_Table("Player")
        return render_template(prefix + 'Matches.html', matches=match_data, players=players)   
    
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

        if all(name in players for name in team1_players) and all(name in players for name in team2_players):
            try:
                create_match_and_players(team1_players, team2_players, team1_score, team2_score,match_date)
                flash('Your form was successfully submitted!', 'success')
            except Exception as e:
                flash(e, 'error')
        else:
            missing_from_team1 = [name for name in team1_players if name not in players]
            missing_from_team2 = [name for name in team2_players if name not in players]
            flash(f"missing_from_team1: {missing_from_team1}, missing_from_team2: {missing_from_team2}", 'error')
        return redirect(url_for('Babyfoot_Add_Match'))

    @app.route(prefix + 'rankings')
    def babyfoot_rankings():
        Matches_Data = Request_Matches(None) or []
        global_ranking = {}
        one_v_one = {}
        two_v_two_solo_score = {}
        two_v_two_team_score = {}
        others = {}

        def update_score(score_dict, player, is_win):
            score_dict.setdefault(player, [0, 0, None])
            score_dict[player][1] += 1
            if is_win:
                score_dict[player][0] += 1
            if score_dict[player][1] != 0:
                score_dict[player][2] = (score_dict[player][0] / score_dict[player][1]) * 100

        for match in Matches_Data:
            id, sc1, sc2, date, team1, team2 = match

            team1_names = team1.split(",")
            team2_names = team2.split(",")
            if len(team1_names) == len(team2_names) == 1:
                update_score(one_v_one, team1,sc1 > sc2)
                update_score(one_v_one, team2,sc2 > sc1)
            elif len(team1_names) == len(team2_names) == 2:
                for player in team1_names:
                    update_score(two_v_two_solo_score, player,sc1 > sc2)
                for player in team2_names:
                    update_score(two_v_two_solo_score, player,sc2 > sc1)
                update_score(two_v_two_team_score, team1,sc1 > sc2)
                update_score(two_v_two_team_score, team2,sc2 > sc1)
            else:
                for player in team1_names:
                    update_score(others, player,sc1 > sc2)
                for player in team2_names:
                    update_score(others, player,sc2 > sc1)

            for player in team1_names:
                update_score(global_ranking, player,sc1 > sc2)
            for player in team2_names:
                update_score(global_ranking, player,sc2 > sc1)


        def convert(arr):
            return sorted( [[key] + values[0:2] + [f"{values[-1]:.2f}"] for key, values in arr.items() if values[-1] is not None], key=lambda x: float(x[-1]), reverse=True)

        args = {
            "global_ranking": convert(global_ranking),
            "one_v_one": convert(one_v_one),
            "two_v_two_solo_score": convert(two_v_two_solo_score),
            "two_v_two_team_score": convert(two_v_two_team_score),
            "others": convert(others)
        }
        return render_template(prefix + 'rankings.html', **args)
    