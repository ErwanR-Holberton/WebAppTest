#!/usr/bin/env python3
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

def log(message):
    with open('request_logs.log', 'a') as f:
        print(message)
        f.write(message + "\n")

"""@app.before_request
def log_request_info():
    try:
        log_message = "Request Info: "

        log(request.url)
        log(request.headers)
        log(request.remote_addr)
        log(request.form)
        log(request.method)

    except Exception as e:
        log(str(e))"""

@app.route('/')
def hello():
    print("hello")
    return 'V1'

@app.route('/flan')
def flan():
    return 'flan de pate'

@app.route('/index')
def index():
    return render_template('3.html')

@app.route('/flutter')
def flutter():
    print("main")
    return send_from_directory('./templates', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    print(filename)
    return send_from_directory('./templates', filename)

@app.route('/gpt')
def gpt():
    return render_template('gpt.html')

@app.route('/youarehere')
def youarehere():
    return render_template('youarehere.html')

@app.route('/laval')
def laval():
    with open('/home/ERHBTN/WebAppTest/Amenities.txt', 'r') as file:
        data = file.read()
    return data

if __name__ == '__main__':
    app.run(port=8080)
