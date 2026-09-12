"""Tiny local server for the JARVIS V2 eDEX + 4D VRM UI preview."""
from __future__ import annotations

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse


class NoCacheHandler(SimpleHTTPRequestHandler):
    """Disable browser caching during UI development."""

    def end_headers(self) -> None:  # pragma: no cover - exercised manually
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=4173)
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    server = ThreadingHTTPServer(("127.0.0.1", args.port), NoCacheHandler)
    server.RequestHandlerClass.directory = str(root)
    print(f"JARVIS UI: http://127.0.0.1:{args.port}/index.html")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
