import random
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

dt = 1

data = [
    ["Fred"         , "C24", "1983", "M", "1.78m", "5", "Fondamentaux 1"],
    ["Henri"        , "C24", "1994", "M", "1.86m", "5", "Fondamentaux 1"],
    ["Medhi"        , "C24", "1999", "M", "1.71m", "3", "Fondamentaux 1"],
    ["Stéphane"     , "C24", "1977", "M", "1.83m", "4", "Fondamentaux 1"],

    ["Erwan L"      , "C23", "1988", "M", "1.73m", "4", "Fondamentaux 2"],
    ["Tifenn"       , "C23", "1992", "M", "1.78m", "3", "Fondamentaux 2"],
    ["Marc C"       , "C23", "1991", "M", "1.82m", "5", "Fondamentaux 2"],
    ["Nicolas"      , "C23", "1990", "M", "1.87m", "5", "Fondamentaux 2"],
    ["Antonin"      , "C23", "1998", "M", "1.67m", "3", "Fondamentaux 2"],
    ["Joshua"       , "C23", "1995", "M", "1.80m", "2", "Fondamentaux 2"],
    ["Tarek"        , "C23", "1990", "M", "1.80m", "3", "Fondamentaux 2"],

    ["Florian M"    , "C22", "1991", "M", "1.70m", "1", "Fondamentaux 3"],

    ["Erwan R"      , "C21", "1996", "M", "1.80m", "2", "AR/VR"],
    ["Kévin"        , "C21", "1991", "M", "1.74m", "3", "AR/VR"],
    ["Gaël"         , "C21", "1987", "M", "1.69m", "1", "AR/VR"],
    ["Arnaud  "     , "C20", "2001", "M", "1.69m", "0.5", "AR/VR"],

    ["Alexandre G"  , "C21", "1994", "M", "1.72m", "4", "FS"],
    ["Nathalie"     , "C21", "1990", "F", "1.60m", "2.5", "FS"],
    ["Benjamin"     , "C20", "1989", "M", "1.72m", "1", "FS"],

    ["Erwan C"      , "C21", "1984", "M", "1.84m", "0", "RNCP"],
    ["Nadège"       , "C21", "1987", "F", "1.58m", "0", "RNCP"],

    ["Charlotte"  , "Staff", "1995", "F", "1.79m", "5", "Staff"],
]

def handle_size(text):
    return float(text[:4])

def get_true_false_plus_minus(index, user):
    if index == 4:
        usersize = handle_size(user[index])
        choicesize = handle_size(holberdle_game.choice[index])
        if usersize > choicesize:
            return "minus"
        elif usersize < choicesize:
            return "plus"
        elif usersize == choicesize:
            return "True"
    elif index in [2, 5]:
        userval = float(user[index])
        choiceval = float(holberdle_game.choice[index])
        if userval > choiceval:
            return "minus"
        elif userval < choiceval:
            return "plus"
        elif userval == choiceval:
            return "True"
    else:
        if user[index] == holberdle_game.choice[index]:
            return "True"
    return "False"

def make_array(user):
    send = []
    for i in range(len(user)):
        send.append(get_true_false_plus_minus(i, user))
    return send

def get_time():
    return datetime.now().replace(minute=0, second=0, microsecond=0)

class holberdle_game:
    choice = [None]
    start_time = get_time()

    @classmethod
    def new_game(cls):
        cls.start_time = get_time()
        cls.choice = data[random.randint(0, len(data) - 1)]

@app.route("/")
def holberdle():
    if (get_time() + timedelta(hours=dt) > holberdle_game.start_time):
        holberdle_game.new_game()
    return render_template('index.html', target_time=holberdle_game.start_time + timedelta(hours=dt))

@app.route("/new_game")
def holberdle_new_game():
    holberdle_game.new_game()
    return 'OK', 200

@app.route("/get_names")
def holberdle_get_names():
    names = []
    for user in data:
        names.append(user[0])
    return jsonify(names)

@app.route("/check_name", methods=['POST'])
def holberdle_check_name():
    result = request.get_json()
    name = result['name']
    for user in data:
        if user[0] == name:
            return jsonify(user, make_array(user))
    return jsonify("error")

holberdle_game.new_game()


if __name__ == "__main__":
    app.run()
