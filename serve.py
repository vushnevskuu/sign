#!/usr/bin/env python3
"""Простой сервер для статики. Камера — в браузере, без доступа сервера."""
import http.server
import socketserver
import os

os.chdir(os.path.join(os.path.dirname(__file__), "static"))
PORT = 8765

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Сервер: http://localhost:{PORT}")
    print("Камера работает в браузере — разрешите доступ при запросе.")
    httpd.serve_forever()
