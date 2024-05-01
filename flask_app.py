#!/usr/bin/env python3
from flask import Flask, render_template, request

app = Flask(__name__)

def log(message):
    with open('request_logs.log', 'a') as f:
        f.write(message + "\n")

@app.before_request
def log_request_info():
    try:
        log(str(request))
    except Exception as e:
        log(e)

@app.route('/')
def hello():
    return 'V1'

@app.route('/flan')
def flan():
    return 'flan de pate'

@app.route('/index')
def index():
    return render_template('3.html')

if __name__ == '__main__':
    app.run(port=8080)
