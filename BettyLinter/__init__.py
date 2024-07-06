from flask import Flask, render_template
import subprocess
import os
from sys import argv

if "--local" not in argv:
    server_ip = "erhbtn.pythonanywhere.com"
else:
    server_ip = "127.0.0.1:5000"

app = Flask(__name__)

def file_save(text):
    with open("file.c", "w+") as file:
        file.write(text)

def run_betty_style_check(text):
    routebetty = os.path.join("..", "Betty", "betty-style.pl")
    file_save(text)
    command = "{} file.c 2>&1".format(routebetty)  # Escape single quotes in the text
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)
    return result.stdout

def run_betty_doc_check(text):
    routebetty = os.path.join("..", "Betty", "betty-doc.pl")
    file_save(text)
    command = "{} file.c 2>&1".format(routebetty)  # Escape single quotes in the text
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)
    return result.stdout

@app.route("/")
def indexbetty():
    return render_template("index.html", address=server_ip)

@app.route("/validate", methods=['POST'])
def templatebetty():
    print("validating")
    data = request.get_json()
    code = data.get('code', '')

    betty = run_betty_style_check(code)
    betty_doc = run_betty_doc_check(code)
    result = {"style": betty, "doc": betty_doc}
    print("validating end")
    return jsonify(result=result)


if __name__ == '__main__':
    app.run(debug=True)
