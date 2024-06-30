from flask import Flask, render_template, jsonify, request
from sys import argv


app = Flask(__name__)


if "--local" not in argv:
    server_ip = "erhbtn.pythonanywhere.com"
else:
    server_ip = "127.0.0.1:5000"
