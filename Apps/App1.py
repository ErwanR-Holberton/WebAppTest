from FlaskApp import *
prefix = "/App1/"

def routes():
    print("other", __name__)
    @app.route(prefix)
    def index1():
        return "hello 1"

    @app.route(prefix + 'template')
    def template1():
        return render_template(prefix + "index.html")
