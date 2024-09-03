if __name__ != "__main__":
    from FlaskApp import *
prefix = "/CheckerInjection/"

data = []


def routes():
    @app.route(prefix)
    def index_CheckerInjection():
        return render_template(prefix + 'index.html', data=data)

    @app.route(prefix + 'send', methods=['POST'])
    def send_data_CheckerInjection():
        print(request.data.decode("UTF-8"))
        print(dir(request))
        data.append(request.data.decode("utf-8"))
        return "OK"