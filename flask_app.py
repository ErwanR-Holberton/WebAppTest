#!/usr/bin/env python3
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {}  # Dictionary to keep track of connected users

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

@app.route('/Chat')
def Chat():
    return render_template('Chat.html')

@socketio.on('message')
def handle_message(msg):
    new_msg = str(users[request.sid]) + ': ' + msg
    print(new_msg)
    send(new_msg, broadcast=True)

@socketio.on('connect')
def handle_connect():
    username = request.args.get('username')
    users[request.sid] = username
    emit('user_list', list(users.values()), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        del users[request.sid]
        emit('user_list', list(users.values()), broadcast=True)

@app.route('/laval')
def laval():
    with open('/home/ERHBTN/WebAppTest/Laval.json', 'r') as file:
        data = file.read()
    return data

if __name__ == '__main__':
    socketio.run(app, debug=True)
    """app.run(port=8080)"""
