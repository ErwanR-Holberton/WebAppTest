#!/usr/bin/env python3
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {}  # Dictionary to keep track of connected users
history = ""

def log(message):
    with open('request_logs.log', 'a') as f:
        print(message)
        f.write(message + "\n")

def log2(object1, object2=""):
    global history
    msg = str(object1)
    if object2 != "":
        msg += ": " + str(object2)
        if str(object2) not in ["None", "True", "False", "", "<"]:
            if not str(object2).startswith('<'):
                print(msg)
                history += msg + "</br>"
    else:
        print(msg)
        history += msg + "</br>"

@app.before_request
def history_log():
    if request.path != "/history":
        log2(str(request.method) +" " + str(request.url))
        log2(str(request.host) +" " + str(request.host_url))
        log2("from: " + str(request.remote_addr))
        log2("Route: " + str(request.path))
        log2("Data: " + str(request.get_data()))
        """    for attr in dir(request):
            if not attr.startswith('_'):
                try:
                    log2(attr, getattr(request, attr))
                except:
                    pass"""
        log2("")

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
    log2(new_msg)
    send(new_msg, broadcast=True)

@socketio.on('connect')
def handle_connect():
    username = request.args.get('username')
    users[request.sid] = username
    log2("connection: " + str(username) + " " + str(request.sid) + "</br>")
    emit('user_list', list(users.values()), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        log2("disconnection: " + str(users[request.sid]) + " " + str(request.sid) + "</br>")
        del users[request.sid]
        emit('user_list', list(users.values()), broadcast=True)

@app.route('/history')
def history_route():
    return history

@app.route('/laval')
def laval():
    with open('/home/ERHBTN/WebAppTest/Laval.json', 'r') as file:
        data = file.read()
    return data

if __name__ == '__main__':
    socketio.run(app, debug=True)
    """app.run(port=8080)"""
