#!/usr/bin/env python3
from sanic import Sanic
from sanic.response import json
from websockets.exceptions import ConnectionClosedError
import websockets
import asyncio

app = Sanic("ChatServer")
clients = set()

@app.route('/')
async def index(request):
    return json({"message": "Welcome to the chat server!"})

async def chat_handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except ConnectionClosedError:
        pass
    finally:
        clients.remove(websocket)

async def start_websocket_server():
    server = await websockets.serve(chat_handler, "0.0.0.0", 8001)
    await server.wait_closed()

@app.listener('after_server_start')
async def websocket_server(app, loop):
    loop.create_task(start_websocket_server())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
