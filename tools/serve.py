# -*- coding: utf-8 -*-
"""Serve the repo, and accept a rendered frame back from the page.

Comparing a model to a reference by looking at both is what produced three builds that were
not close. This lets the render come back as a FILE, so the same measurement code runs over
the reference and over our own output and the two are compared as numbers.
"""
import base64
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = r'C:\Users\Alex\Desktop\Oran_Personal_Brand\portfolio-repo'
SHOTS = os.path.dirname(os.path.abspath(__file__))


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_POST(self):
        if not self.path.startswith('/save/'):
            self.send_error(404)
            return
        name = os.path.basename(self.path[6:]) or 'shot.png'
        n = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(n).decode('ascii', 'replace')
        if ',' in raw:
            raw = raw.split(',', 1)[1]
        open(os.path.join(SHOTS, name), 'wb').write(base64.b64decode(raw))
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'ok')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def end_headers(self):
        if not self.path.startswith('/save/'):
            self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, *a):
        pass


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8732
    ThreadingHTTPServer(('127.0.0.1', port), H).serve_forever()
