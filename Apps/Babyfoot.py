from FlaskApp import *
prefix = "/Babyfoot/"
import mysql.connector
from DB_CONFIG import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE

db_config = {
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'host': MYSQL_HOST,
    'database': MYSQL_DATABASE,
    'port': 3306,
}

def Read_Table(table_name):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM {table_name};".format(table_name=table_name)
    cursor.execute(query)
    result = cursor.fetchall()


    cursor.close()
    connection.close()
    return result[0]


def routes():
    @app.route(prefix)
    def Babyfoot():
        return "Nothing to see, it's a DB"

    @app.route(prefix + 'PUT', methods=['PUT'])
    def Babyfoot_add_match():
        try:
            words = request.json.get('words', [])

            if not isinstance(words, list):
                return jsonify({'error': 'Invalid input format. Expected JSON array.'}), 400

            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            for word, vector in words:
                insert_query = "INSERT INTO words (word, vector) VALUES (%s, %s);"
                cursor.execute(insert_query, (word, vector))
                count += 1

            connection.commit()
            cursor.close()
            connection.close()

            return 'ok', 200

        except mysql.connector.Error as err:
            return f"Error accessing MySQL: {err}", 500

    @app.route(prefix + "QUERY", methods=['POST'])
    def DB_Baby_QUERY():
        try:
            data = request.json
            words_to_query = data.get('words', [])

            word_dict = {word: None for word in words_to_query}

            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            query = "SELECT word, vector FROM words WHERE word IN (%s)" % ','.join(['%s'] * len(words_to_query))
            cursor.execute(query, words_to_query)
            result = cursor.fetchall()

            cursor.close()
            connection.close()

            for word, vector in result:
                word_dict[word] = vector

            return jsonify(word_dict)

        except mysql.connector.Error as err:
            return f"Error accessing MySQL: {err}", 500

    @app.route(prefix + "Players")
    def Babyfoot_Players():
        players = Read_Table("words")
        return render_template(prefix + "Players.html", players=players)
