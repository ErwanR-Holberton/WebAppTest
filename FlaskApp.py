from flask import Flask, render_template, jsonify, request, url_for, redirect, flash
from sys import argv


app = Flask(__name__)


if "--local" in argv:
    server_ip = "127.0.0.1:5000"
elif "--github" in argv:
    server_ip = "opulent-palm-tree-5gvvjj969rwf4j6p-5000.app.github.dev"
else:
    server_ip = "erhbtn.pythonanywhere.com"
