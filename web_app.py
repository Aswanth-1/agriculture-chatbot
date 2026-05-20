import json
import mimetypes
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from command_handler import build_welcome_payload, get_bot_response

# paths
BASE_DIR = Path(__file__).parent
WEB_DIR = BASE_DIR / "web"


class AgricultureWebHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = self.path

        # welcome API
        if path == "/api/welcome":
            data = build_welcome_payload()
            self.send_json(data)
            return

        # serve index page
        if path == "/" or path == "/index.html":
            self.serve_file(WEB_DIR / "index.html")
            return

        # serve css
        if path == "/styles.css":
            self.serve_file(WEB_DIR / "styles.css")
            return

        # serve js
        if path == "/app.js":
            self.serve_file(WEB_DIR / "app.js")
            return

        # not found
        self.send_json({"error": "page not found"}, 404)

    def do_POST(self):
        path = self.path

        if path != "/api/chat":
            self.send_json({"error": "not found"}, 404)
            return

        # read request body
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            body = {}
        else:
            raw = self.rfile.read(length)
            try:
                body = json.loads(raw.decode("utf-8"))
            except Exception:
                self.send_json({"error": "bad JSON"}, 400)
                return

        message = str(body.get("message", ""))
        history = body.get("history", [])

        if not isinstance(history, list):
            history = []

        reply = get_bot_response(message, history)
        self.send_json({"reply": reply})

    def serve_file(self, filepath):
        if not filepath.exists():
            self.send_json({"error": "file not found"}, 404)
            return

        content_type = mimetypes.guess_type(str(filepath))[0]
        if content_type is None:
            content_type = "text/plain"

        data = filepath.read_bytes()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # disable default logging
        pass


def main():
    host = "127.0.0.1"
    port = 8000
    url = f"http://{host}:{port}"
    server = HTTPServer((host, port), AgricultureWebHandler)
    print(f"Server started at {url}")
    print("Opening browser...")
    webbrowser.open_new(url)
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    server.server_close()


if __name__ == "__main__":
    main()


MyHandler = AgricultureWebHandler
