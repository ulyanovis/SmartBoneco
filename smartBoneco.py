from http.server import BaseHTTPRequestHandler, HTTPServer
# import SocketServer
import json
import cgi
import time


class Server(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def _set_headers(self):
        self.send_response(200)
        #self.protocol_version = 'HTTP/1.1'
        self.send_header('Content-type', 'application/json')
        #self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-length', '19')
        self.end_headers()

    #def handle_one_request(self):
        #super(Server, self).handle_one_request()

        #self.server.sessions.pop(self.client_address)

    def do_HEAD(self):
        self._set_headers()

    # GET sends back a Hello world message
    def do_GET(self):
        time.sleep(0.1)
        print(self.requestline, self.headers)
        self._set_headers()
        self.wfile.write((json.dumps({'humidity': 50.5}) + '\n').encode())
        self.close_connection = False
        #self.finish()
        #self.wfile.write("<html><body><h1>hi!</h1></body></html>".encode())

    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # read the message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        # add a property to the object, just to mess with data
        message['received'] = 'ok'

        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(message).encode())

    #def log_message(self, format, *args):
    #    return


def run(server_class=HTTPServer, handler_class=Server, port=1880):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)


    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
