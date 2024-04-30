#!/usr/bin/env python3
from flask import Flask, request, render_template
import json
from waitress import serve

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('3.html')

serve(app, host="0.0.0.0", port=8080)
