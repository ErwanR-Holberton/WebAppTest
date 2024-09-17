from FlaskApp import *
import os, random, string, base64

prefix = "/Holbertus/"

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_dir, 'Tusmo.txt')

def load_motus_words():
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines() if all(c in string.ascii_uppercase for c in line.strip())]

def pick_word():
    return random.choice(load_motus_words())

def routes():
    @app.route(prefix)
    def index_Holbertus():
        return render_template(prefix + 'menu.html')
    
    @app.route(prefix + "mot_du_jour")
    def holbertus_mot_du_jour():
        word = pick_word()
        print(word)
        coded_word = base64.b64encode(word.encode()).decode('utf-8')
        return render_template(prefix + 'word.html', word=word, coded_word=coded_word)

