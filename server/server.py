import json
import os
import socket
import sys
from .views import router
from .manager import Manager
from models.text_markov import TextMarkov


class Server:
    def __init__(self, config_path, router):

        # Load config file
        with open(config_path) as config_file:
            self.config = json.load(config_file)

        # Load active models into memory
        self.manager = Manager(self.config['data_directory'])

        # Attach views
        self.router = router

        # Set up network server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name, port = self.config['host_name'], self.config['port']
        self.sock.bind((host_name, port))
        self.sock.listen(5)

    def get_request(self):
        '''Get the next request. This method returns a pair: (connection,
        request), where connection is a socket and request is the contents of
        the request (parsed from JSON into into a Python object).
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

        return connection, json.loads(request_string)

    def run(self):
        while True:
            connection, request = self.get_request()
            command = request['command']
            args = request.get('args', {})
            try:
                result = self.router.views[command](manager=self.manager, **args)
                response = json.dumps({
                    'status': 'success',
                    'result': result
                })
            except Exception as e:
                raise e
                response = json.dumps({
                    'status': 'error',
                    'result': str(e)
                })
            connection.sendall(response.encode('utf-8'))
            connection.close()
