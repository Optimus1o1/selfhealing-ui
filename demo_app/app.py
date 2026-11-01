from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from typing import Optional


V1_HTML = """<!DOCTYPE html>
<html>
<head>
    <title>E-Commerce Demo V1</title>
    <style>
        body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f0f2f5; }
        .card { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 320px; }
        .form-group { margin-bottom: 1rem; }
        input { width: 100%; padding: 8px; box-sizing: border-box; }
        .btn-primary { background: #2563eb; color: white; border: none; padding: 10px; width: 100%; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Sign In (V1)</h2>
        <form action="/dashboard" method="GET">
            <div class="form-group">
                <input type="text" id="username" name="username" placeholder="Username" required />
            </div>
            <div class="form-group">
                <input type="password" id="password" name="password" placeholder="Password" required />
            </div>
            <button type="submit" id="loginBtn" class="btn-primary">Login</button>
        </form>
    </div>
</body>
</html>"""

V2_HTML = """<!DOCTYPE html>
<html>
<head>
    <title>E-Commerce Demo V2 (Refactored)</title>
    <style>
        body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #0F1013; color: #F2EFE8; }
        .auth-container { background: #17191E; border: 1px solid #2A2D35; padding: 2.5rem; border-radius: 12px; width: 340px; }
        .field { margin-bottom: 1.2rem; }
        input { width: 100%; padding: 10px; background: #22262F; border: 1px solid #363B47; color: white; border-radius: 6px; box-sizing: border-box; }
        .btn-submit-brand { background: #E0A45C; color: #0F1013; font-weight: bold; border: none; padding: 12px; width: 100%; border-radius: 6px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="auth-container">
        <h2>Customer Portal (V2)</h2>
        <form action="/dashboard" method="GET" id="authForm">
            <div class="field">
                <input type="text" id="userEmail" name="username" placeholder="Email Address" required />
            </div>
            <div class="field">
                <input type="password" id="userSecret" name="password" placeholder="Password" required />
            </div>
            <!-- Refactored element: ID changed to signinBtn, class changed, label changed to 'Sign In' -->
            <button type="submit" id="signinBtn" class="btn-submit-brand" data-testid="auth-submit">Sign In</button>
        </form>
    </div>
</body>
</html>"""

EDGE_CASES_HTML = """<!DOCTYPE html>
<html>
<head>
    <title>Edge Cases Diagnostic</title>
</head>
<body>
    <h2>Actionability & Ambiguity Diagnostics</h2>
    
    <!-- 1. Hidden Button -->
    <button id="hiddenButton" style="display: none;">Invisible Target</button>
    
    <!-- 2. Disabled Button -->
    <button id="disabledButton" disabled>Disabled Target</button>
    
    <!-- 3. Duplicate Ambiguous Buttons -->
    <button class="ambiguous-btn">Duplicate Action</button>
    <button class="ambiguous-btn">Duplicate Action</button>
</body>
</html>"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
</head>
<body>
    <h1 id="welcomeHeader">Welcome to Dashboard</h1>
    <p>Authentication was successful.</p>
</body>
</html>"""


class DemoAppHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silence default logging during test runs
        return

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/v1"):
            self._respond(V1_HTML)
        elif path == "/v2":
            self._respond(V2_HTML)
        elif path == "/edge_cases":
            self._respond(EDGE_CASES_HTML)
        elif path == "/dashboard":
            self._respond(DASHBOARD_HTML)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def _respond(self, html: str):
        content = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


class DemoServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 8899):
        self.host = host
        self.port = port
        self.server: Optional[HTTPServer] = None
        self.thread: Optional[threading.Thread] = None

    def start(self):
        self.server = HTTPServer((self.host, self.port), DemoAppHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()


if __name__ == "__main__":
    import time
    server = DemoServer("127.0.0.1", 8899)
    print("Serving Demo App at http://127.0.0.1:8899 (V1: /v1, V2: /v2, Edge Cases: /edge_cases)")
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
