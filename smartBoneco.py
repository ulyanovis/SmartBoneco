from http.server import BaseHTTPRequestHandler, HTTPServer
# import SocketServer
import json
import cgi
import logging
from tion import TionApi, Breezer, Zone, MagicAir
import time

email, password = 'funtik007@list.ru', 'Puse4ka7'

class Server(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def _set_headers(self, size: int = 0):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-length', str(size))
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    # GET sends back a Hello world message
    def do_GET(self):
        CO2Sensor.load()
        payload = json.dumps({'humidity': CO2Sensor.humidity}) + '\n'
        # payload = json.dumps({'humidity': 15.15}) + '\n'
        self._set_headers(len(payload))
        self.wfile.write(payload.encode())
        self.close_connection = False


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

    api = TionApi(email, password, auth_fname=None)
    CO2Sensor = api.get_devices()[3]
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
