#!/usr/bin/env python3
"""CGL+ ExamKit local host: serves the web app and persists its browser data in SQLite."""
from __future__ import annotations
import json, os, re, socket, sqlite3, sys, threading, secrets, ipaddress
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, unquote

APP_DIR = Path(__file__).resolve().parent
PORT = int(os.environ.get("EXAMKIT_PORT", "8765"))
HOSTNAME = re.sub(r"[^a-z0-9-]", "-", os.environ.get("EXAMKIT_HOSTNAME") or socket.gethostname().split(".")[0].lower()).strip("-") or "examkit"
DATA_ROOT = Path(os.environ.get("EXAMKIT_DATA_DIR") or (
    Path(os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA") or Path.home()) / "CGL" / "ExamKit" if sys.platform == "win32" else
    Path.home() / "Library" / "Application Support" / "CGL ExamKit" if sys.platform == "darwin" else
    Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "cgl-examkit"
))
DATA_ROOT.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_ROOT / "examkit.sqlite3"
TOKEN_PATH = DATA_ROOT / "server-token"
if TOKEN_PATH.exists():
    TOKEN = TOKEN_PATH.read_text(encoding="utf-8").strip()
else:
    TOKEN = secrets.token_urlsafe(32)
    TOKEN_PATH.write_text(TOKEN, encoding="utf-8")
try:
    TOKEN_PATH.chmod(0o600)
except OSError:
    pass

def db():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
    return conn

def snapshot():
    conn = db()
    try:
        return dict(conn.execute("SELECT key,value FROM kv"))
    finally:
        conn.close()

def replace_snapshot(values):
    if not isinstance(values, dict) or len(values) > 5000:
        raise ValueError("Invalid storage snapshot")
    clean = {}
    total = 0
    for key, value in values.items():
        if not isinstance(key, str) or not re.match(r"^(os:|examkit:)", key):
            raise ValueError("Unexpected storage key")
        if not isinstance(value, str):
            raise ValueError("Storage values must be strings")
        total += len(key.encode()) + len(value.encode())
        if total > 32 * 1024 * 1024:
            raise ValueError("Storage snapshot exceeds 32 MB")
        clean[key] = value
    conn = db()
    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute("DELETE FROM kv")
        conn.executemany("INSERT INTO kv(key,value) VALUES(?,?)", clean.items())
        conn.commit()
    finally:
        conn.close()

def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.0.2.1", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    def log_message(self, fmt, *args):
        print("[ExamKit] " + (fmt % args))

    def send_json(self, status, data):
        raw = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def authorized(self):
        return secrets.compare_digest(self.headers.get("X-ExamKit-Token", ""), TOKEN)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/state":
            if not self.authorized():
                return self.send_json(401, {"error": "Unauthorized"})
            return self.send_json(200, {"storage": snapshot()})
        if path in ("/", "/index.html"):
            html = (APP_DIR / "index.html").read_text(encoding="utf-8")
            html = html.replace("/*EXAMKIT_SERVER_BOOTSTRAP*/", "window.__EXAMKIT_SERVER_REQUIRED__=true;")
            raw = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(raw)
            return
        return super().do_GET()

    def do_PUT(self):
        if urlparse(self.path).path != "/api/state":
            return self.send_json(404, {"error": "Not found"})
        if not self.authorized():
            return self.send_json(401, {"error": "Unauthorized"})
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size < 2 or size > 32 * 1024 * 1024:
                return self.send_json(413, {"error": "Invalid payload size"})
            payload = json.loads(self.rfile.read(size))
            replace_snapshot(payload.get("storage"))
            return self.send_json(200, {"ok": True})
        except Exception as exc:
            return self.send_json(400, {"error": str(exc)})

def announce():
    try:
        from zeroconf import ServiceInfo, Zeroconf
        ip = local_ip()
        info = ServiceInfo(
            "_http._tcp.local.",
            f"ExamKit OS ({HOSTNAME})._http._tcp.local.",
            addresses=[socket.inet_aton(ip)],
            port=PORT,
            properties={"path": "/", "product": "CGL+ ExamKit OS"},
            server=f"{HOSTNAME}.local."
        )
        zc = Zeroconf()
        zc.register_service(info)
        print(f"[ExamKit] mDNS service announced on {HOSTNAME}.local")
        return zc, info
    except Exception as exc:
        print(f"[ExamKit] mDNS announcement unavailable: {exc}")
        print("[ExamKit] You can still open the LAN address shown below.")
        return None, None

if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    zc, service = announce()
    ip = local_ip()
    print("")
    print("CGL+ ExamKit OS is running.")
    print(f"  This computer: http://localhost:{PORT}")
    print(f"  Local network: http://{HOSTNAME}.local:{PORT}")
    print(f"  LAN fallback:  http://{ip}:{PORT}")
    print(f"  Data folder:   {DATA_ROOT}")
    print(f"  Host access key: {TOKEN}")
    print("  Enter this key in the browser on each device that connects.")
    print("  Keep this terminal open while using ExamKit. Press Ctrl+C to stop.")
    print("")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[ExamKit] Shutting down...")
    finally:
        server.server_close()
        if zc and service:
            zc.unregister_service(service)
            zc.close()
