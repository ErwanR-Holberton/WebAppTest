#!/usr/bin/env python3
from flask import Flask, render_template, request

app = Flask(__name__)

def log(message):
    with open('request_logs.log', 'a') as f:
        print(message)
        f.write(message + "\n")

@app.before_request
def log_request_info():
    try:
        log_message = "Request Info: "
        """log(f"Request: {str(request)}, Method: {request.method}, URL: {request.url}, Headers: {request.headers}, Remote Address: {request.remote_addr}, Form Data: {request.form}, Query Parameters: {request.args}, JSON Data: {request.json}, Cookies: {request.cookies}, Files: {request.files}, Path: {request.path}, Full Path: {request.full_path}, Scheme: {request.scheme}, Base URL: {request.base_url}, User Agent: {request.user_agent}")
        """
        log(request.url)
        log(request.headers)
        log(request.remote_addr)
        log(request.form)
        log(request.method)

        """for attr in dir(request):                               # Iterate over attributes of the request object

            if not attr.startswith('_'):                        # Skip private attributes and methods


                if attr == 'json':
                    continue
                value = getattr(request, attr)                  # Get the value of the attribute
                if value is None:
                    continue
                print(attr, value)
                log_message += "{}: {},".format(attr, value)    # Add the attribute and its value to the log message

        log(str(log_message))"""

    except Exception as e:
        log(str(e))

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
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8080)
