import danmu
import time
import asyncio
import _thread
import threading
import http
from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer

class UnityHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=UTF-8")
        self.end_headers()
        for recv in danmu.douyu.listRecv:
            self.wfile.write(bytes(str(recv), encoding="UTF-8"))
        danmu.douyu.listRecv.clear()
    def __call__(self):
        pass

def main():
    server_address = ('localhost', 8000)
    handler_class = UnityHTTPRequestHandler
    server_class = HTTPServer
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

_thread.start_new_thread(danmu.main)
_thread.start_new_thread(main)

while True:
    pass