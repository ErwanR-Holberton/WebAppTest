from FlaskApp import *
prefix = "/BettyLinter/"

import subprocess
import os


def file_save(text):
    with open("file.c", "w+") as file:
        file.write(text)

def run_betty_style_check(text):
    routebetty = os.path.join("..", "Betty", "betty-style.pl")
    file_save(text)
    command = "{} file.c".format(routebetty)  # Escape single quotes in the text
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)
    return result.stdout

def run_betty_doc_check(text):
    routebetty = os.path.join("..", "Betty", "betty-doc.pl")
    file_save(text)
    command = "{} file.c".format(routebetty)  # Escape single quotes in the text
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)
    return result.stdout

def routes():
    @app.route(prefix)
    def indexbetty():
        return render_template(prefix + "index.html", address=server_ip)

    @app.route(prefix + 'validate', methods=['POST'])
    def templatebetty():
        data = request.get_json()
        code = data.get('code', '')

        betty = run_betty_style_check(code)
        betty_doc = run_betty_doc_check(code)
        result = {style: betty, doc: betty_doc}
        return jsonify(result=result)
