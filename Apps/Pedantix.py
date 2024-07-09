#!/usr/bin/env python3
from FlaskApp import *
prefix = "/Pedantix/"
import re, string
from datetime import datetime, timedelta
import math, requests
dt = 1

class DB:
    database_path = 'skip1000-100.txt'
    loaded_words = {}

    def load_db():
        url = f'https://drive.usercontent.google.com/download?id=1Mkb7NKOMNV8buxI6gbd8DyTlMuw62iWN&export=download&confirm=t&uuid=7ab09d9e-d08a-4265-a637-2b433db9f605'
        response = requests.get(url)
        content = response.content.decode().splitlines()

        loaded_words = {}
        for line in content:
            parts = line.split()
            word = parts[0]
            vector = list(map(float, parts[1:]))
            loaded_words[word] = vector
        return loaded_words

    @classmethod
    def load_vectors(cls, words):
        cls.loaded_words = {}
        with open(cls.database_path, 'r') as f:
            for line in f:
                parts = line.split()
                word = parts[0]
                if word in words:
                    vector = list(map(float, parts[1:]))
                    cls.loaded_words[word] = vector
        return cls.loaded_words

    @classmethod
    def load_vector(cls, word):
        with open(cls.database_path, 'r') as f:
            for line in f:
                parts = line.split()
                if word == parts[0]:
                    return list(map(float, parts[1:]))
        return None

    @classmethod
    def cosine_similarity(cls, vec1, vec2):
        dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(v ** 2 for v in vec1))
        magnitude2 = math.sqrt(sum(v ** 2 for v in vec2))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0  # Handle division by zero
        return dot_product / (magnitude1 * magnitude2)

    @classmethod
    def compare_words(cls, word1, word2):
        vector1 = cls.load_vector(word1)
        vector2 = cls.load_vector(word2)
        if vector1 is None or vector2 is None:
            return None
        return cls.cosine_similarity(vector1, vector2)

    @classmethod
    def get_all_similarity(cls, word1):
        result = []
        vec1 = cls.load_vector(word1)
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

    @classmethod
    def get_all_similarity_new(cls, word1):
        result = []
        vec1 = cls.loaded_words.get(word1)
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
        """DB.loaded_words = DB.load_db()"""

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
        res = DB.get_all_similarity_new(word)
        return jsonify(res)



