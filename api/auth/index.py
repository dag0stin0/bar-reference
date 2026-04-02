"""OAuth initiation endpoint for Decap CMS GitHub backend."""

import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlencode


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_id = os.environ.get("GITHUB_CLIENT_ID", "")
        params = urlencode({
            "client_id": client_id,
            "scope": "repo,user",
            "response_type": "code",
        })
        self.send_response(302)
        self.send_header("Location", f"https://github.com/login/oauth/authorize?{params}")
        self.end_headers()
