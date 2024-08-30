if __name__ != "__main__":
    from FlaskApp import *
prefix = "/Personnal_Website/"


def routes():
    @app.route(prefix)
    def index_Personnal_website():
        return render_template(prefix + 'index.html')

    @app.route('/Personnal_Website/assets/<path:filename>')
    def serve_assets(filename):
        # Redirect all old asset links to the correct static folder
        return redirect(url_for('static', filename=f'{prefix[1:]}assets/{filename}'))
