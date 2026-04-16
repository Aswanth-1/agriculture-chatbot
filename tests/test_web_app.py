import json
import socket
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from http.server import ThreadingHTTPServer

from web_app import AgricultureWebHandler


class WebAppTests(unittest.TestCase):
    def setUp(self):
        sock = socket.socket()
        sock.bind(("127.0.0.1", 0))
        self.port = sock.getsockname()[1]
        sock.close()

        self.server = ThreadingHTTPServer(("127.0.0.1", self.port), AgricultureWebHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=1)

    def _url(self, path):
        return f"http://127.0.0.1:{self.port}{path}"

    def test_welcome_endpoint_returns_expected_payload(self):
        with urlopen(self._url("/api/welcome")) as response:
            payload = json.loads(response.read().decode("utf-8"))

        self.assertEqual(payload["title"], "AgriFlow Assistant")
        self.assertIn("quick_actions", payload)
        self.assertIn("message", payload)

    def test_chat_endpoint_returns_guided_response(self):
        request = Request(
            self._url("/api/chat"),
            data=json.dumps(
                {
                    "message": "weather",
                    "history": [],
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request) as response:
            payload = json.loads(response.read().decode("utf-8"))

        self.assertTrue(payload["reply"].startswith("Weather Update:"))

    def test_chat_history_command_uses_prior_messages_only(self):
        request = Request(
            self._url("/api/chat"),
            data=json.dumps(
                {
                    "message": "history",
                    "history": ["weather"],
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request) as response:
            payload = json.loads(response.read().decode("utf-8"))

        self.assertEqual(payload["reply"], "Command History:\n1. weather")

    def test_stylesheet_route_serves_live_styles(self):
        with urlopen(self._url("/styles.css")) as response:
            content_type = response.headers.get("Content-Type", "")
            body = response.read().decode("utf-8")

        self.assertIn("text/css", content_type)
        self.assertIn(".chat-widget", body)

    def test_invalid_json_returns_bad_request(self):
        request = Request(
            self._url("/api/chat"),
            data=b"{",
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with self.assertRaises(HTTPError) as context:
            urlopen(request)

        self.assertEqual(context.exception.code, 400)
        context.exception.close()


if __name__ == "__main__":
    unittest.main()
