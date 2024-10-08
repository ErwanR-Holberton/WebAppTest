from flask import Flask, render_template, jsonify, request, url_for, redirect, flash
from sys import argv


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

SERVER_ADDRESS = "http://erhbtn.pythonanywhere.com"

LOCAL_MODE = True


if "--local" in argv:
    server_ip = "127.0.0.1:5000"
elif "--github" in argv:
    server_ip = "opulent-palm-tree-5gvvjj969rwf4j6p-5000.app.github.dev"
else:
    server_ip = "erhbtn.pythonanywhere.com"
    LOCAL_MODE = False
