from FlaskApp import *
prefix = "/DB/"
import mysql.connector
from DB_CONFIG import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE

db_config = {
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'host': MYSQL_HOST,
    'database': MYSQL_DATABASE,
    'port': 3306,
}

def routes():
    @app.route(prefix)
    def indexDB():
        return "Nothing to see, it's a DB"

    @app.route(prefix + "READ")
    def DB_READ():
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            query = "SELECT word, vector FROM words;"
            cursor.execute(query)

            words = cursor.fetchall()

            cursor.close()
            connection.close()

            # Render a template to display the words
            return render_template(prefix + 'words.html', words=words)

        except mysql.connector.Error as err:
            return f"Error accessing MySQL: {err}"

    @app.route(prefix + 'PUT', methods=['PUT'])
    def add_words():
        try:
            words = request.json.get('words', [])

            if not isinstance(words, list):
                return jsonify({'error': 'Invalid input format. Expected JSON array.'}), 400

            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            datalen = len(words)
            count = 0

            for word, vector in words:
                insert_query = "INSERT INTO words (word, vector) VALUES (%s, %s);"
                cursor.execute(insert_query, (word, vector))
                count += 1

            connection.commit()
            cursor.close()
            connection.close()

            return 'ok', 200

        except mysql.connector.Error as err:
            return f"Error accessing MySQL: {err}\n{datalen}, {count}", 500
