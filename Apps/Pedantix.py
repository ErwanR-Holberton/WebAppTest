#!/usr/bin/env python3
from FlaskApp import *
prefix = "/Pedantix/"
import re, string

def get_wiki_page():
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

    title = get_random_wiki_name()
    return title, get_wikipedia_page_text(title)

def get_headers():
    title, text = get_wiki_page()
    sections = re.split(r'\n== .* ==\n', text)
    headings = re.findall(r'\n== (.*) ==\n', text)
    return title, headings


class pedantix_game:

    @classmethod
    def new_game(cls):
        cls.title, cls.text = get_wiki_page()
        cls.format_text(cls.title, cls.text)

    @classmethod
    def format_text(cls, title, text):

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


        full_text = title + " ==\n" + text
        sections = re.split(r'\n\n== |\n\n=== ', full_text)
        pair_head_text = []
        for s in sections:
            elements = re.split(r' ==\n| ===\n', s)
            pair_head_text.append(elements)
            pair_head_text[-1][1] = tokenize(pair_head_text[-1][1])
        print(pair_head_text)

        cls.array = pair_head_text

    @classmethod
    def get_jinja_args(cls):
        args = {}
        args['text'] = cls.array
        return args

pedantix_game.new_game()


@app.route(prefix)
def hello_world():
    return render_template('index.html', **pedantix_game.get_jinja_args())



