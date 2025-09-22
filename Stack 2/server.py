import asyncio
import websockets
import http.server
import socketserver
import threading
import socket
import json

# --- Obtener la IP local ---
hostname = socket.gethostname()
LOCAL_IP = socket.gethostbyname(hostname)

# --- Servidor HTTP ---
HTTP_PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=".", **kwargs)

def start_http():
    with socketserver.TCPServer(("0.0.0.0", HTTP_PORT), Handler) as httpd:
        print(f"Servidor HTTP en http://{LOCAL_IP}:{HTTP_PORT}")
        httpd.serve_forever()

# --- Servidor WebSocket ---
WS_PORT = 8765
clients = {}

async def notify_all(message):
    if clients:
        data = json.dumps(message, ensure_ascii=False)
        await asyncio.gather(*(ws.send(data) for ws in clients))

async def websocket_handler(ws):
    try:
        async for raw in ws:
            try:
                msg = json.loads(raw)
            except:
                continue

            if msg.get("type") == "join":
                username = msg.get("username", "Anon")
                clients[ws] = username
                print(f"[JOIN] {username}")
                await notify_all({
                    "type": "system",
                    "subtype": "join",
                    "username": username,
                    "text": f"{username} se ha unido."
                })

            elif msg.get("type") == "message":
                username = clients.get(ws, "Anon")
                text = msg.get("text", "")
                print(f"[MSG] {username}: {text}")
                await notify_all({
                    "type": "message",
                    "username": username,
                    "text": text
                })
    except websockets.ConnectionClosed:
        pass
    finally:
        if ws in clients:
            username = clients.pop(ws)
            print(f"[LEAVE] {username}")
            await notify_all({
                "type": "system",
                "subtype": "leave",
                "username": username,
                "text": f"{username} se ha desconectado."
            })

async def start_websocket():
    async with websockets.serve(websocket_handler, "0.0.0.0", WS_PORT):
        print(f"Servidor WebSocket en ws://{LOCAL_IP}:{WS_PORT}")
        await asyncio.Future()

# --- Main ---
if __name__ == "__main__":
    threading.Thread(target=start_http, daemon=True).start()
    asyncio.run(start_websocket())
