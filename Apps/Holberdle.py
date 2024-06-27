from FlaskApp import *
prefix = "/Holberdle/"

data = [
    ["user1", "C21", "1995", "M", "1.80", "5", "AR/VR"],
    ["user2", "C20", "1990", "F", "1.70", "4", "FS"],
    ["user3", "C21", "2000", "M", "1.60", "3", "3e trimestre"],
    ["user4", "C21", "1910", "M", "1.850", "2", "AR/VR"]
]

def routes():
    @app.route(prefix)
    def holberdle():
        return render_template(prefix + 'index.html')

    @app.route(prefix + "get_names")
    def holberdle_get_names():
        names = []
        for user in data:
            name.append(user[0])
        return jsonify(names)
