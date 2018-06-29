from http.server import HTTPServer
from server import RequestHandler

if __name__ == "__main__":
    SERVER = HTTPServer(('localhost', 8000), RequestHandler)
    print("[INFO]Starting server at localhost:8000...")
    SERVER.serve_forever()

