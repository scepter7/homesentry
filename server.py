from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import json
import os

from md_manager import start_md


class RequestHandler(BaseHTTPRequestHandler):
    """Custom Request Handler for commands from Telegram Bot."""

    def do_GET(self):
        """GET handler."""

        self.send_response(200)
        self.end_headers()
        return

    def do_POST(self):
        """POST handler. Process Telegram Bot commands."""

        content_len = int(self.headers.get("content-length"))
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body)

        if data["command"] == "creds":
            os.environ["TG_TOKEN"] = data["api"]
            os.environ["chat_id"] = data["chat_id"]
            self.send_response(200)
            self.end_headers()
        elif data["command"] == "sentry":
            print("[INFO]Starting Motion Detector...")

            t = Thread(target=start_md)
            t.daemon = True
            t.start()

            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
        return
