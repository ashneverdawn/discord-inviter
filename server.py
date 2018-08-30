from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        if "eid" in query:
            eid = query["eid"][0]
            print(eid)

            redirect = 'https://discordapp.com/'
            html = '<head><meta http-equiv="Refresh" content="0; url=' + redirect + '"></head>'

            self.send_response(200)
            self.end_headers()
            self.wfile.write(html.encode())


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()