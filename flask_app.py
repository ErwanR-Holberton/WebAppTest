#!/usr/bin/env python3
from sanic import Sanic, response
from sanic.response import json
from sanic.request import Request
import asyncio

app = Sanic("LongPollingChat")
messages = []

@app.route('/')
async def index(request):
    return await response.file('Sanichat.html')

@app.route('/send', methods=['POST'])
async def send_message(request: Request):
    message = request.json.get('message')
    if message:
        messages.append(message)
    return json({"status": "Message received"})

@app.route('/poll')
async def poll_messages(request: Request):
    last_index = int(request.args.get('last_index', 0))
    new_messages = messages[last_index:]

    if new_messages:
        return json({"messages": new_messages, "new_index": len(messages)})

    # If no new messages, wait for a new message
    while True:
        await asyncio.sleep(1)
        new_messages = messages[last_index:]
        if new_messages:
            return json({"messages": new_messages, "new_index": len(messages)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
