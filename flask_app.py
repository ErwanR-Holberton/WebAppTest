from flask import Flask, jsonify
import os
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import sys

sys.setrecursionlimit(100)
address = "localhost:5000"
server_ip = address
links = ""


os.system("cls")
app = Flask(__name__)
apps = {}
ignore_dirs = ['__pycache__', 'main.py', '.git', 'old_files', '.gitignore']

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

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, application)
