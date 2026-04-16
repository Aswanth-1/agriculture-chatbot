import argparse
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from command_handler import build_welcome_payload, get_bot_response

PROJECT_ROOT = Path(__file__).resolve().parent
WEB_DIR = PROJECT_ROOT / "web"
STATIC_ROUTES = {
    "/": WEB_DIR / "index.html",
    "/styles.css": WEB_DIR / "styles.css",
    "/app.js": WEB_DIR / "app.js",
}


class AgricultureWebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        route = parsed_path.path

        if route == "/api/welcome":
            self._send_json(build_welcome_payload())
            return

        file_path = STATIC_ROUTES.get(route)

        if file_path is None or not file_path.exists():
            self._send_json({"error": "Not found."}, status_code=404)
            return

        self._send_file(file_path)

    def do_POST(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path != "/api/chat":
            self._send_json({"error": "Not found."}, status_code=404)
            return

        payload = self._read_json_payload()

        if payload is None:
            self._send_json({"error": "Invalid JSON payload."}, status_code=400)
            return

        message = str(payload.get("message", ""))
        history = payload.get("history", [])
        if not isinstance(history, list):
            history = []

        response = {
            "reply": get_bot_response(message, history),
        }
        self._send_json(response)

    def log_message(self, format_string, *args):
        return

    def _read_json_payload(self):
        content_length = int(self.headers.get("Content-Length", "0"))

        if content_length == 0:
            return {}

        raw_body = self.rfile.read(content_length)

        try:
            return json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            return None

    def _send_file(self, file_path):
        content_type, _ = mimetypes.guess_type(str(file_path))
        content_type = content_type or "application/octet-stream"
        file_bytes = file_path.read_bytes()
        content_type_header = content_type

        if content_type.startswith("text/") or content_type in {
            "application/javascript",
            "application/json",
            "application/xml",
            "image/svg+xml",
        }:
            content_type_header = f"{content_type}; charset=utf-8"

        self.send_response(200)
        self.send_header("Content-Type", content_type_header)
        self.send_header("Content-Length", str(len(file_bytes)))
        self.end_headers()
        self.wfile.write(file_bytes)

    def _send_json(self, payload, status_code=200):
        response_body = json.dumps(payload).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)


def run_server(host="127.0.0.1", port=8000):
    server = ThreadingHTTPServer((host, port), AgricultureWebHandler)
    print(f"Agriculture website running at http://{host}:{port}")
    print("Press Ctrl+C to stop the server.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description="Run the Agriculture Chatbot website.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind the web server to.")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the web server to.")
    args = parser.parse_args()
    run_server(args.host, args.port)


if __name__ == "__main__":
    main()
