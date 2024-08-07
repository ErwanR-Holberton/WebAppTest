from flask import Flask, jsonify, request
import os, sys
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from sys import argv

if "--local" not in argv:
    address = "erhbtn.pythonanywhere.com"
else:
    address = "127.0.0.1:5000"

links = ""

if os.name == "nt":
    os.system("cls")
    print("The operating system is Windows")
elif os.name == "posix":
    os.system("clear")
    print("The operating system is Linux or macOS")
else:
    print(f"The operating system is {os.name}")

app = Flask(__name__)
apps = {}
ignore_dirs = ['__pycache__', 'flask_app.py', '.git', 'old_files', '.gitignore', 'templates']

original_cwd = os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=================================start loop==================================================")
for app_folder in os.listdir('./'):
    if app_folder in ignore_dirs:
        continue
    print(app_folder)
    module = __import__(app_folder)
    app_name = getattr(module, "app")
    apps[f'/{app_folder}'] = app_name
    print(app_folder)
    links += f"<a href='http://{address}/{app_folder}/'>http://{address}/{app_folder}/</a><br>"

application = DispatcherMiddleware(app, apps)


@app.route('/')
def index():
    return links

def print_routes(app):
    for rule in app.url_map.iter_rules():
        print(f"Endpoint: {rule.endpoint}, URL: {rule}")

@app.before_request
def log_request_info():
    print(f"Request Path: {request.path}")


print(apps)
for azerty in apps.values():
    print_routes(azerty)
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, application)
