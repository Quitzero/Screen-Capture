import http.server
import socketserver

HOST = 'localhost'
PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler


def run_server():
    with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        print(HOST, PORT)
        httpd.serve_forever()


run_server()
