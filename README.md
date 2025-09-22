# 💬 UniChat — Messenger con WebSockets

UniChat es un sistema de mensajería en tiempo real que funciona en la red local utilizando **WebSockets** y **HTML**.  
Incluye dos versiones del proyecto:

1. **Versión básica (solo WebSockets)**: el cliente abre directamente el archivo `index.html` en su navegador y se conecta al servidor WebSocket.  
2. **Versión con HTTP + WebSockets**: el servidor levanta un servicio HTTP para servir el frontend y un servicio WebSocket en paralelo. Esta versión detecta automáticamente la IP del servidor, facilitando la conexión desde otros dispositivos.

---

## 🚀 Tecnologías utilizadas
- **Python 3** — Lenguaje de programación para el servidor.  
- **[websockets](https://websockets.readthedocs.io/)** — Librería de Python para implementar el protocolo WebSocket.  
- **asyncio** — Librería estándar de Python para manejar concurrencia asíncrona.  
- **HTML5 + CSS3 + JavaScript** — Interfaz de usuario moderna y responsive (similar a un messenger).  
- **HTTP Server (módulos estándar de Python)** — Solo en la versión 2, para servir el archivo `index.html`.  

---

## 📂 Estructura del proyecto

uniChat/
│
├── version1_ws_only/
│ ├── server.py # Servidor WebSocket
│ └── index.html # Cliente (frontend)
│
├── version2_http_ws/
│ ├── server.py # Servidor HTTP + WebSocket
│ └── index.html # Cliente (frontend)
│
└── README.md
