import json
import os
import sys
from .views import router
from models.text_markov import TextMarkov


class Server:
    def __init__(self, config_path, router):

        # Load config file from disk
        self.config_path = config_path
        with open(config_path) as config_file:
            self.config = json.load(config_file)

        # Load active models into memory
        self.models = {}
        for model_name, model_config in self.config['models'].items():
            if model_config['active']:
                n = model_config['n']
                tokenizer = model_config['tokenizer']
                self.models[model_name] = TextMarkov(n, tokenizer)

                graph_path = model_config['path']
                with open(graph_path) as graph_file:
                    self.models[model_name].graph = json.load(graph_file)

        self.router = router

    def save_config(self):
        with open(self.config_path, 'w') as config_file:
            json.dump(self.config, config_file)

    def save_graph(self, model_name):
        graph_path = self.config['models'][model_name]['path']
        with open(graph_path, 'w') as graph_file:
            json.dump(self.models[model_name].graph, graph_file)

    def run(self):
        for line in sys.stdin:  # FIXME: This should be generalized to other input sources
            request = json.loads(line)
            command = request['command']
            args = request.get('args', {})
            try:
                result = self.router.views[command](server=self, **args)
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
