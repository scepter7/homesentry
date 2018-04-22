from http.server import HTTPServer
from threading import Thread

from server import RequestHandler
from md_manager import start_md


if __name__ == "__main__":

    server = HTTPServer(('localhost', 8000), RequestHandler)
    print("[INFO]Starting server at localhost:8000...")
    server.serve_forever()