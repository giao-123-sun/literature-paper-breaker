#!/usr/bin/env python3
"""Simple HTTP server for the paper visualization dashboard."""
import http.server
import os
import sys

PORT = 8080

# Serve from project root so output/ files are accessible
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def log_message(self, format, *args):
        pass  # Quiet mode

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    with http.server.HTTPServer(('0.0.0.0', port), Handler) as httpd:
        print(f"Dashboard: http://localhost:{port}")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()
