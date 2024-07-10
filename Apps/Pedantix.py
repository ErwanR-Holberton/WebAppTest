#!/usr/bin/env python3
from FlaskApp import *
import re, string, math, requests, json, mysql.connector
from datetime import datetime, timedelta
from DB_CONFIG import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE

prefix = "/Pedantix/"
db_config = {
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'host': MYSQL_HOST,
    'database': MYSQL_DATABASE,
    'port': 3306,
}
dt = 1

class DB:
    loaded_words = {}

    def QUERY_SERVER(words):
        try:
            word_dict = {word: None for word in words}

            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            query = "SELECT word, vector FROM words WHERE word IN (%s)" % ','.join(['%s'] * len(words_to_query))
            cursor.execute(query, words_to_query)
            result = cursor.fetchall()

            cursor.close()
            connection.close()

            for word, vector in result:
                word_dict[word] = [float(x) for x in json.loads(vector)]

            return word_dict

        except mysql.connector.Error as err:
            print("QUERY ERROR:", err)
            return None

    def QUERY_LOCAL(words):
        url = "http://erhbtn.pythonanywhere.com/DB/QUERY"

        data = {"words": words}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            result = response.json()
            print(type(result))
            for word, vector in result.items():
                if vector is not None:
                    result[word] = [float(x) for x in json.loads(vector)]
            return result
        else:
            print("Failed to get response. Status code:", response.status_code)
            print("Response text:", response.text)

    def QUERY(words):
        if server_ip == "127.0.0.1:5000":
            print("local setup")
            return DB.QUERY_LOCAL(words)
        elif server_ip == "erhbtn.pythonanywhere.com":
            print("server setup")
            return DB.QUERY_SERVER(words)
        print("wrong server ip ?")
        return None

    def load_or_query(word):
        vec = DB.loaded_words.get(word)
        if vec is not None:
            return vec

        result = DB.QUERY([word])
        if result[word] is None:
            return None
        return result[word]

    @classmethod
    def cosine_similarity(cls, vec1, vec2):
        print(vec1, vec2)
        dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(v ** 2 for v in vec1))
        magnitude2 = math.sqrt(sum(v ** 2 for v in vec2))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0  # Handle division by zero
        return dot_product / (magnitude1 * magnitude2)

    @classmethod
    def get_all_similarity(cls, word1):
        result = []
        vec1 = cls.load_or_query(word1)
        if vec1 is None:
            return None
        for word2, id_len in pedantix_game.word_mapping.items():
            vec2 = cls.loaded_words.get(word2)
            id2 = id_len[0]
            if vec2 is not None:
                sim = cls.cosine_similarity(vec1, vec2)
                if sim == 1:
                    sim = word2
            else:
                sim = None
            result.append([id2, sim])
        return result


def get_wiki_page(title=None):
    import requests
    from urllib.parse import unquote

    def get_random_wiki_name(): #returns title with spécial chars no underscore
        response = requests.get("https://fr.wikipedia.org/wiki/Special:Random")
        response.raise_for_status()
        title = response.url.split('/')[-1]
        return unquote(title).replace('_', ' ')

    def get_wikipedia_page_text(title):
        url = "https://fr.wikipedia.org/w/api.php"

        # Parameters for the API request
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "titles": title,
            "explaintext": True,  # Get plain text extract
        }

        # Send the request to the Wikipedia API
        response = requests.get(url, params=params)
        response.raise_for_status()
        # Extract the page text
        pages = response.json()["query"]["pages"]
        page = next(iter(pages.values()))  # Get the first page (there should be only one)

        # Check if the page was found
        if "extract" in page:
            return page["extract"]
        else:
            return "Page not found"

    if title is None:
        title = get_random_wiki_name()

    return title, get_wikipedia_page_text(title)

def get_time():
    return datetime.now().replace(minute=0, second=0, microsecond=0)

def categorize(ch):
    if ch in string.ascii_letters:
        return "word"
    if ch in "é":
        return "word"
    if ch in string.digits:
        return "digit"
    if ch in string.punctuation:
        return "punct"
    if ch in [' ']:
        return "punct"
    if ch in ['\n']:
        return "\n"
    return "word"

class pedantix_game:
    start_time = None

    @classmethod
    def new_game(cls):
        cls.start_time = get_time()
        cls.title, cls.text = get_wiki_page("Alphonse Michon-Dumarais")
        cls.format_text(cls.title, cls.text)
        cls.make_data_set()
        DB.loaded_words = DB.QUERY([w for w in cls.words])


    @classmethod
    def format_text(cls, title, text):


        def tokenize(text):
            tokens = []
            state = None
            word = ""
            for ch in text:
                cat = categorize(ch)
                if cat != state:
                    if word != "":
                        tokens.append(word)
                    word = ""
                    state = cat
                    if cat == "error":
                        pass
                word += ch

            tokens.append(word)
            return tokens

        ban_list = ["Liens externes", "Notes et références", "Sources", "Lien externe"]

        full_text = title + " ==\n" + text
        sections = re.split(r'\n\n== |\n\n=== ', full_text)
        pair_head_text = []
        for s in sections:
            elements = re.split(r' ==\n| ===\n', s)
            if elements[0] not in ban_list and elements[1] != '':
                pair_head_text.append(elements)
                pair_head_text[-1][0] = tokenize(pair_head_text[-1][0])
                pair_head_text[-1][1] = tokenize(pair_head_text[-1][1])
                """print(pair_head_text[-1])"""

        cls.array = pair_head_text

    @classmethod
    def get_jinja_args(cls):
        args = {}
        args['text'] = cls.array
        args['pairs'] = cls.pair_id_len
        args['words'] = cls.word_mapping
        args['dataset'] = cls.data_set
        return args

    @classmethod
    def make_data_set(cls):

        def extract_words(arr, word_set=None):
            if word_set is None:
                word_set = set()

            if isinstance(arr, list):
                for item in arr:
                    extract_words(item, word_set)
            else:
                word_set.add(arr)

            return word_set

        def create_word_mapping(words):
            return {word: [i, len(word)] for i, word in enumerate(words)}

        def replace_words_with_ids(arr, word_mapping):
            if isinstance(arr, list):
                return [replace_words_with_ids(item, word_mapping) for item in arr]
            else:
                return word_mapping[arr]

        def make_pairs(words, word_mapping):
            return [word_mapping[w] + ["<br>"] if categorize(w[0]) == "\n" else word_mapping[w] + ["hidden"] if categorize(w[0]) != "punct" else word_mapping[w] + [w] for w in words]
        """print(cls.text)
        print(cls.array)"""
        cls.words = words = extract_words(cls.array)
        """print(words)"""
        cls.word_mapping = create_word_mapping(words)
        """print(cls.word_mapping)"""

        cls.pair_id_len = make_pairs(words, cls.word_mapping)
        """print(cls.pair_id_len)"""

        cls.data_set = replace_words_with_ids(cls.array, cls.word_mapping)
        """print(cls.data_set)"""


def routes():

    @app.route(prefix)
    def pedantix():
        if (pedantix_game.start_time is None or get_time() > pedantix_game.start_time + timedelta(hours=dt)):
            pedantix_game.new_game()
        return render_template(prefix + 'index.html', **pedantix_game.get_jinja_args())

    @app.route(prefix + "guess", methods=['POST'])
    def pedantix_guess():
        result = request.get_json()
        word = result['word']
        res = DB.get_all_similarity(word)
        return jsonify(res)



