"""OAuth callback endpoint for Decap CMS GitHub backend."""

import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        code = query.get("code", [""])[0]

        if not code:
            self.send_response(400)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Missing code parameter")
            return

        # Exchange code for access token
        data = json.dumps({
            "client_id": os.environ.get("GITHUB_CLIENT_ID", ""),
            "client_secret": os.environ.get("GITHUB_CLIENT_SECRET", ""),
            "code": code,
        }).encode()

        req = Request(
            "https://github.com/login/oauth/access_token",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

        resp = urlopen(req)
        result = json.loads(resp.read().decode())
        token = result.get("access_token", "")

        # Decap CMS expects a postMessage with the token
        body = f"""<!DOCTYPE html>
<html><body><script>
(function() {{
  function receiveMessage(e) {{
    console.log("receiveMessage %o", e);
    window.opener.postMessage(
      'authorization:github:success:{{"token":"{token}","provider":"github"}}',
      e.origin
    );
  }}
  window.addEventListener("message", receiveMessage, false);
  window.opener.postMessage("authorizing:github", "*");
}})();
</script></body></html>"""

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(body.encode())
