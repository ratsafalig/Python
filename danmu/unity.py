import http

def run(server_class=http.server.HTTPServer, handler_class=http.server.BaseHTTPRequestHandler):
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

class UnityHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        pass
    def do_GET(self):
        self.send_response(200)
        body = b"hello world"
        Content_Length = len(body)
        self.send_header('Content-Length', Content_Length)
        self.end_headers()
        self.wfile.write(body)

run(http.server.HTTPServer, UnityHTTPRequestHandler)

