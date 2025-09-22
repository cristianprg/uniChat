#!/usr/bin/env python3
# server.py
# Requisitos: pip install websockets
# Ejecutar: python3 server.py
# Escucha por defecto en 0.0.0.0:8765 para acceptar conexiones desde la red local.

import asyncio
import websockets
import json
from datetime import datetime

HOST = "0.0.0.0"   # aceptar conexiones desde cualquier IP (LAN)
PORT = 8765

# Conjuntos de websockets conectados y mapa websocket->username
CONNECTED = set()
USERNAMES = dict()

def now_iso():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def broadcast(obj):
    """Enviar objeto (dict) a todos los clientes conectados en JSON."""
    if not CONNECTED:
        return
    data = json.dumps(obj, ensure_ascii=False)
    await asyncio.gather(*(ws.send(data) for ws in CONNECTED))


async def handler(ws):
    # Registrar conexión
    CONNECTED.add(ws)
    print(f"[{now_iso()}] Nueva conexión: {ws.remote_address}")
    try:
        # Esperamos que el cliente mande un mensaje tipo 'join' con su username
        async for raw in ws:
            try:
                msg = json.loads(raw)
            except Exception:
                # si no es json, ignorar
                continue

            t = msg.get("type")
            if t == "join":
                username = msg.get("username", "Anon")
                USERNAMES[ws] = username
                print(f"[{now_iso()}] {username} se ha unido desde {ws.remote_address}")
                await broadcast({
                    "type": "system",
                    "subtype": "join",
                    "username": username,
                    "time": now_iso(),
                    "text": f"{username} se ha unido."
                })
            elif t == "message":
                username = USERNAMES.get(ws, "Anon")
                text = msg.get("text", "")
                timestamp = now_iso()
                payload = {
                    "type": "message",
                    "username": username,
                    "text": text,
                    "time": timestamp
                }
                print(f"[{timestamp}] {username}: {text}")
                await broadcast(payload)
            elif t == "ping":
                # cliente puede enviar pings periódicos; opcional
                await ws.send(json.dumps({"type": "pong"}))
            else:
                # mensaje desconocido -> ignorar o log
                print(f"[{now_iso()}] Mensaje no reconocido: {msg}")
    except websockets.ConnectionClosedOK:
        pass
    except websockets.ConnectionClosedError:
        pass
    except Exception as e:
        print(f"[{now_iso()}] Error: {e}")
    finally:
        # desconexión: eliminar y notificar
        username = USERNAMES.pop(ws, None)
        CONNECTED.discard(ws)
        if username:
            print(f"[{now_iso()}] {username} se ha desconectado")
            await broadcast({
                "type": "system",
                "subtype": "leave",
                "username": username,
                "time": now_iso(),
                "text": f"{username} se ha desconectado."
            })
        else:
            print(f"[{now_iso()}] Conexión cerrada: {ws.remote_address}")


async def main():
    print(f"Servidor WebSocket arrancando en ws://{HOST}:{PORT} ...")
    async with websockets.serve(handler, HOST, PORT, ping_interval=20, ping_timeout=20):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor detenido por teclado.")
