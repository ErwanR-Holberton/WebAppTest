from FlaskApp import *
import os, random, string, base64

prefix = "/Holbertus/"

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_dir, 'ods6.txt')

def load_motus_words(min_length=5, max_length=50):
    with open(file_path, "r") as file:
        return [
            line.strip() 
            for line in file.readlines() 
            if min_length <= len(line.strip()) <= max_length
        ]

def pick_word():
    return random.choice(load_motus_words())

def routes():
    @app.route(prefix)
    def index_Holbertus():
        return render_template(prefix + 'menu.html')
    
    @app.route(prefix + "mot_du_jour")
    def holbertus_mot_du_jour():
        word = pick_word()
        coded_word = base64.b64encode(word.encode()).decode('utf-8')
        return render_template(prefix + 'word.html', word=word, coded_word=coded_word)
    

    @app.route(prefix + "check_word", methods=['POST'])
    def holbertus_check_word():
        word = request.get_json().get('word')
        words = load_motus_words()
        if word in words:
            return "OK"
        else:
            return f"{word} not in dictionary"
    


