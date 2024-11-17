if __name__ != "__main__":
    from FlaskApp import *
prefix = "/HolbertonBowlingVRWebGL/"



def routes():
    @app.route(prefix)
    def index_Bowling():
        return render_template(prefix + 'index.html')

    @app.route(prefix + 'TemplateData/<path:filename>')
    def serve_templatedata(filename):
        # Redirect all old asset links to the correct static folder
        return redirect(url_for('static', filename=f'{prefix[1:]}TemplateData/{filename}'))

    @app.route(prefix + 'Build/<path:filename>')
    def serve_Build(filename):
        # Redirect all old asset links to the correct static folder
        return redirect(url_for('static', filename=f'{prefix[1:]}Build/{filename}'))
