
if __name__ != "__main__":
    from FlaskApp import *
import random
prefix = "/Holberdle/"

data = [
    ["Florian M"    , "C22", "1991", "M", "1.70m", "1", "Fondamenteaux"],
    ["Erwan R"      , "C21", "1996", "M", "1.80m", "2", "AR/VR"],
    ["Alexandre G"  , "C21", "1994", "M", "1.72m", "4", "FS"],
    ["Nathalie"     , "C21", "1990", "F", "1.60m", "2.5", "FS"],
    ["Stéphane"     , "C24", "1977", "M", "1.83m", "4", "Fondamenteaux 1"],
    ["Tarek"        , "C23", "1990", "M", "1.80m", "3", "Fondamenteaux 2"],
    ["Fred"         , "C24", "1983", "M", "1.78m", "5", "Fondamenteaux 1"],
    ["Henri"        , "C24", "1994", "M", "1.86m", "5", "Fondamenteaux 1"],
    ["Medhi"        , "C24", "1999", "M", "1.71m", "3", "Fondamenteaux 1"],
    ["Kévin"        , "C21", "1991", "M", "1.74m", "3", "AR/VR"],
    ["Erwan C"      , "C21", "1991", "M", "1.74m", "0", "Diplomé(e)"],
    ["Nadège"       , "C21", "1987", "F", "1.58m", "0", "Diplomé(e)"]
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


class holberdle_game:
    choice = [None]

    @classmethod
    def new_game(cls):
        cls.choice = data[random.randint(0, len(data) - 1)]

def routes():
    @app.route(prefix)
    def holberdle():
        return render_template(prefix + 'index.html')

    @app.route(prefix + "new_game")
    def holberdle_new_game():
        holberdle_game.new_game()
        return 'OK', 200

    @app.route(prefix + "get_names")
    def holberdle_get_names():
        names = []
        for user in data:
            names.append(user[0])
        return jsonify(names)

    @app.route(prefix + "check_name", methods=['POST'])
    def holberdle_check_name():
        print(holberdle_game.choice)
        result = request.get_json()
        name = result['name']
        for user in data:
            if user[0] == name:
                return jsonify(user, make_array(user))
        return jsonify("error")

    holberdle_game.new_game()


if __name__ == "__main__":
    from flask import Flask, render_template, jsonify, request
    app = Flask(__name__)
    routes()
    app.run()
