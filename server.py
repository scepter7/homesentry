from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import json

from md_manager import start_md


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        return
    

    def do_POST(self):
        content_len = int(self.headers.get("content-length"))
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body)

        if data["command"] == "sentry":
            print("[INFO]Starting Motion Detector...")

            t = Thread(target=start_md)
            t.daemon = True
            t.start()

            self.send_response(200)
            self.end_headers()
        elif data["command"] == "getPhoto":
            print("[INFO]Making an image of the room...")
            self.send_response(200)
            self.end_headers()
        elif data["command"] == "stop":
            print("[INFO]Stopping Motion Detector...")
        else:
            self.send_response(404)
            self.end_headers()
        return
