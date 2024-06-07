from FlaskApp import *
prefix = "/BettyLinter/"

def routes():
    @app.route(prefix)
    def indexbetty():
        return render_template(prefix + "index.html")

    @app.route(prefix + 'validate', methods=['POST'])
    def templatebetty():
        data = request.get_json()
        code = data.get('code', '')
        print(code)
        return jsonify(result=code)
