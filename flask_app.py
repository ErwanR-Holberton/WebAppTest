#!/usr/bin/env python3
from sanic import Sanic, response
from sanic.response import json
import asyncio

app = Sanic("LongPollingChat")
messages = []
clients = []

@app.route('/')
async def index(request):
    return await response.file('Sanichat.html')

@app.route('/send', methods=['POST'])
async def send_message(request):
    message = request.json.get('message')
    if message:
        messages.append(message)
        while clients:
            client = clients.pop()
            client.set_result({"messages": [message]})
    return json({"status": "Message received"})

@app.route('/poll')
async def poll_messages(request):
    last_index = request.args.get('last_index', '0')
    try:
        last_index = int(last_index)
    except ValueError:
        last_index = 0

    new_messages = messages[last_index:]

    if new_messages:
        return json({"messages": new_messages, "new_index": len(messages)})

    # If no new messages, wait for a new message
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    clients.append(future)
    result = await future
    return json(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
