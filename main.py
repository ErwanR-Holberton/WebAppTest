#!/usr/bin/env python3
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, this is a test page!'


@app.route('/index')
def index():
    return render_template('3.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
