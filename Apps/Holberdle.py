from FlaskApp import *
prefix = "/Holberdle/"

def routes():
    @app.route(prefix)
    def holberdle():
        return render_template(prefix + 'index.html')
