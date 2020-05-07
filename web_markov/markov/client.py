import json
import socket
import sys


class Client:
    def __init__(self, host_name, port):
        '''Make a client that consumes the server at host_name:port
        '''
        self.host_name = host_name
        self.port = port

    def _make_request(self, request):
        '''Take a request (a dict with a value for the 'command' key), contact
        the server, and return its request.
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host_name, self.port))

        request_bytes = json.dumps(request).encode('utf-8')
        sock.sendall(request_bytes)
        sock.shutdown(1)

        response_string = ""
        while True:
            chunk = sock.recv(1024)
            if not chunk:
                break
            response_string += chunk.decode('utf-8')
        sock.close()

        return json.loads(response_string)

    def add_model(self, name, n, tokenizer):
        return self._make_request({
            'command': 'add_model',
            'args': {'name': name, 'n': n, 'tokenizer': tokenizer}
        })

    def list_models(self):
        return self._make_request({'command': 'list_models'})

    def delete_model(self, name):
        return self._make_request({
            'command': 'delete_model',
            'args': {'name': name}
        })

    def train_model(self, name, texts):
        return self._make_request({
            'command': 'train_model',
            'args': {'name': name, 'texts': texts}
        })

    def random_text(self, name):
        return self._make_request({
            'command': 'random_text',
            'args': {'name': name}
        })
