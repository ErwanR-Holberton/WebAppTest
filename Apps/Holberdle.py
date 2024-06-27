from FlaskApp import *
prefix = "/Holberdle/"

def routes():
    @app.route(prefix)
    def hello_world():
        return render_template(prefix + 'index.html')



