from FlaskApp import *
prefix = "/PortFolioLinks/"

def routes():
    @app.route(prefix)
    def PF_Links_Index():
        return render_template(prefix + "index.html")