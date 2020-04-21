import json
import os
import socket
import sys
import traceback
from .views import router
from .manager import Manager
from models.text_markov import TextMarkov


class Server:
    '''A server that holds markov models in memory, and allows the client to
    request actions to be performed on them (i.e. train them on new texts,
    generate new random texts with them).

    The server will bind a listening socket to the host name and port defined
    by the 'host_name' and 'port' attributes of the config file. The client
    communicates with the server on a one-socket-connection-per-request basis
    (i.e. HTTP-style). The client should send their request as a JSON object
    encoded in UTF-8, then send a shutdown(1) call, then receive data until the
    server closes the connection on its end (i.e. until it receives a chunk of
    0 bytes).

    Repsonses are also given as UTF-8-encoded JSON objects.
    '''
    def __init__(self, config_path, router):
        # Load config file
        with open(config_path) as config_file:
            self.config = json.load(config_file)

        # Load active models into memory
        self.manager = Manager(self.config['data_directory'])

        # Attach views
        self.router = router

        # Determine debug mode
        self.debug = self.config['debug']

        # Set up network server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name, port = self.config['host_name'], self.config['port']
        self.sock.bind((host_name, port))
        self.sock.listen(5)

    def get_request(self):
        '''Get the next request. This method returns a pair: (connection,
        request), where connection is a socket and request is the contents of
        the request (parsed from JSON into a Python object).
        '''
        connection, address = self.sock.accept()
        print("Accepting connection from %s:%d" % address)
        request_string = ""
        while True:
            chunk = connection.recv(1024)

            # An empty chunk will be received when the client starts shutting
            # down the connection; that means we have received the whole
            # request.
            if not chunk:
                break

            request_string += chunk.decode('utf-8')  # FIXME: Hard-coding as UTF-8: a good idea?

        try:
            request = json.loads(request_string)
        except (UnicodeDecodeError, json.decoder.JSONDecodeError, Exception):
            request = None
        return connection, request

    def send_response(self, connection, response):
        response_string = json.dumps(response)
        connection.sendall(response_string.encode('utf-8'))
        connection.close()

    def run(self):
        while True:
            connection, request = self.get_request()
            if request is None:
                self.send_response(connection, {'status': 'error', 'message': 'bad request'})
                continue
            try:
                command = request['command']
                args = request.get('args', {})
                result = self.router.views[command](manager=self.manager, **args)
                self.send_response(connection, {'status': 'success', 'result': result})
            except Exception as e:
                exception_message = traceback.format_exc()
                print(exception_message)
                if self.debug:
                    message = exception_message
                else:
                    message = 'server-side error'
                self.send_response(connection, {'status': 'error', 'message': message})
