
if __name__ != "__main__":
    from FlaskApp import *
import random
prefix = "/Holberdle/"

data = [
    ["Florian M", "C22", "1991", "M", "1.70m", "1", "Fondamenteaux"],
    ["Erwan R", "C21", "1996", "M", "1.80m", "2", "AR/VR"],
    ["Alexandre G", "C21", "1994", "M", "1.72m", "4", "FS"],
    ["Nathalie", "C21", "1990", "F", "1.60m", "2.5", "FS"],
    ["Stéphane", "C24", "1977", "M", "1.83m", "4", "Fondamenteaux 1"],
    ["Tarek", "C23", "1990", "M", "1.80m", "3", "Fondamenteaux 2"],
    ["Fred", "C24", "1983", "M", "1.78m", "5", "Fondamenteaux 1"],
    ["Henri", "C24", "1994", "M", "1.86m", "5", "Fondamenteaux 1"],
    ["Medhi", "C24", "1999", "M", "1.71m", "3", "Fondamenteaux 1"]
]
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
        send = []
        for user in data:
            if user[0] == name:
                for i in range(len(user)):
                    good = False
                    if user[i] == holberdle_game.choice[i]:
                        good = True
                    send.append(good)
                return jsonify(user, send)
        return jsonify("error")

    holberdle_game.new_game()


if __name__ == "__main__":
    from flask import Flask, render_template, jsonify, request
    app = Flask(__name__)
    routes()
    app.run()
