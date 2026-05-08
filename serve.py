#!/usr/bin/env python3
"""MkDocs serve replacement with working file watching on Python 3.13."""

import http.server
import os
import signal
import socket
import socketserver
import subprocess
import sys
import threading
from pathlib import Path

from watchfiles import watch

DOCS_DIR = Path(__file__).parent / "src"
SITE_DIR = Path(__file__).parent / "site"
HOST = "127.0.0.1"
PORT = 9001


def kill_port(port: int):
    """Kill any process using the given port."""
    try:
        result = subprocess.run(
            ["lsof", "-ti", str(port)], capture_output=True, text=True
        )
        if result.stdout.strip():
            for pid in result.stdout.strip().split("\n"):
                os.kill(int(pid), signal.SIGTERM)
    except Exception:
        pass


def build():
    """Run mkdocs build."""
    subprocess.run(
        [
            sys.executable,
            "-m",
            "mkdocs",
            "build",
            "-f",
            "mkdocs.yml",
            "-d",
            str(SITE_DIR),
        ],
        cwd=Path(__file__).parent,
        check=True,
    )


def serve():
    """Serve the site directory."""
    os.chdir(SITE_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), handler) as httpd:
        httpd.serve_forever()


def main():
    kill_port(PORT)
    print(f"Building documentation...")
    build()
    print(f"Serving on http://{HOST}:{PORT}/")
    print(f"Watching for changes in '{DOCS_DIR}'...")

    # Start HTTP server in background thread
    server_thread = threading.Thread(target=serve, daemon=True)
    server_thread.start()

    # Watch for file changes
    for changes in watch(str(DOCS_DIR), recursive=True):
        print(f"Detected {len(changes)} change(s), rebuilding...")
        build()


if __name__ == "__main__":
    main()
