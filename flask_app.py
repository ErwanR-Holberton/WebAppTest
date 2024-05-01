#!/usr/bin/env python3
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return 'V1'

@app.route('/<path:other>')
def catch_all(other):
    return 'V1 You accessed: %s' % other

@app.route('/index')
def index():
    return render_template('3.html')

if __name__ == '__main__':
    app.run(port=8080)