import json
import os
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

        self.router = router

    def run(self):
        for line in sys.stdin:  # FIXME: This should be generalized to other input sources
            request = json.loads(line)
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
            print(response)  # FIXME: This should be generalized to other outputs
