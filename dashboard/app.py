#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sqlite3
import threading
import webbrowser
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


BASE_DIR = Path(__file__).resolve().parent
APP_SUPPORT_DIR = Path.home() / "Library" / "Application Support" / "GenAIRoadmapDashboard"
DB_PATH = APP_SUPPORT_DIR / "tracker.db"
DASHBOARD_PATH = BASE_DIR / "dashboard.html"
HOST = "127.0.0.1"
PORT = 8765

SEED_COMPLETED = [
    "p0",
    "ph1-c1",
    "ph1-c2",
    "ph1-c3",
    "ph1-c4",
    "ph1-c5",
    "ph1-c6",
    "p1",
    "p2",
    "p3",
    "ph2-c1",
    "ph2-c2",
    "ph2-c3",
]


def is_valid_item_id(item_id: str) -> bool:
    if item_id.startswith("ph") and "-c" in item_id:
        phase, course = item_id[2:].split("-c", 1)
        return phase.isdigit() and course.isdigit()
    if item_id.startswith("p"):
        suffix = item_id[1:]
        return suffix.isdigit() and 0 <= int(suffix) <= 29
    return False


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    APP_SUPPORT_DIR.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS completed_items (
                item_id TEXT PRIMARY KEY,
                completed_at TEXT NOT NULL
            )
            """
        )
        count = conn.execute("SELECT COUNT(*) AS count FROM completed_items").fetchone()["count"]
        if count == 0:
            now = datetime.now(timezone.utc).isoformat()
            conn.executemany(
                "INSERT INTO completed_items (item_id, completed_at) VALUES (?, ?)",
                [(item_id, now) for item_id in SEED_COMPLETED],
            )
        conn.commit()


def get_completed_items() -> list[str]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT item_id FROM completed_items ORDER BY item_id COLLATE NOCASE"
        ).fetchall()
    return [row["item_id"] for row in rows]


def toggle_item(item_id: str) -> list[str]:
    if not is_valid_item_id(item_id):
        raise ValueError(f"Unsupported item id: {item_id}")

    with get_connection() as conn:
        existing = conn.execute(
            "SELECT 1 FROM completed_items WHERE item_id = ?",
            (item_id,),
        ).fetchone()
        if existing:
            conn.execute("DELETE FROM completed_items WHERE item_id = ?", (item_id,))
        else:
            conn.execute(
                "INSERT INTO completed_items (item_id, completed_at) VALUES (?, ?)",
                (item_id, datetime.now(timezone.utc).isoformat()),
            )
        conn.commit()
    return get_completed_items()


class RoadmapHandler(BaseHTTPRequestHandler):
    server_version = "GenAIRoadmap/1.0"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in {"/", "/dashboard.html"}:
            self.serve_dashboard()
            return
        if parsed.path == "/api/state":
            self.send_json({"completed": get_completed_items()})
            return
        if parsed.path == "/healthz":
            self.send_json({"ok": True})
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/api/toggle":
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length) if length else b""
        try:
            payload = json.loads(raw_body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON body"}, status=HTTPStatus.BAD_REQUEST)
            return

        item_id = str(payload.get("id", "")).strip()
        if not item_id:
            self.send_json({"error": "Missing id"}, status=HTTPStatus.BAD_REQUEST)
            return

        try:
            completed = toggle_item(item_id)
        except ValueError as exc:
            self.send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
            return

        self.send_json({"completed": completed})

    def serve_dashboard(self) -> None:
        content = DASHBOARD_PATH.read_text(encoding="utf-8-sig")
        body = content.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.address_string()} - {format % args}")


def open_browser(url: str) -> None:
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the GenAI roadmap tracker.")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", default=PORT, type=int)
    parser.add_argument("--open-browser", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    init_db()
    server = ThreadingHTTPServer((args.host, args.port), RoadmapHandler)
    url = f"http://{args.host}:{args.port}/"
    print(f"GenAI roadmap dashboard running at {url}")
    print(f"SQLite database: {DB_PATH}")
    if args.open_browser:
        open_browser(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping dashboard server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
