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
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = f"SELECT * FROM `{table_name}` LIMIT 10;"
    cursor.execute(query)
    result = cursor.fetchall()


    cursor.close()
    connection.close()
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

def routes():
    @app.route(prefix)
    def Babyfoot():
        return "Nothing to see, it's a DB"

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