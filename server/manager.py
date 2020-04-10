import json
import os
from models.text_markov import TextMarkov


class Manager:
    def __init__(self, data_dir, meta_filename='meta.json'):
        # Create a data directory if one doesn't exist, make a stink if there's
        # something else there
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        elif not os.path.isdir(data_dir):
            raise ValueError("'%s' already exists, and is not a directory!")

        self.meta_path = os.path.join(data_dir, meta_filename)
        self.graph_dir = os.path.join(data_dir, 'graphs')

        # Create an empty markov metadata file if it doesn't exist
        if not os.path.exists(self.meta_path):
            with open(self.meta_path, 'w') as meta_file:
                meta_file.write('{}')

        # Create graphs directory if it doesn't exist
        if not os.path.exists(self.graph_dir):
            os.mkdir(self.graph_dir)

        # Create in-memory equivalent of metadata file
        with open(self.meta_path) as meta_file:
            self.meta = json.load(meta_file)

        # Load active models into memory
        self.active_models = {}
        for model_name, model_meta in self.meta.items():
            if model_meta['active']:
                n = model_meta['n']
                tokenizer = model_meta['tokenizer']
                model = TextMarkov(n=n, tokenizer=tokenizer)

                graph_path = self._get_graph_path(model_name)
                with open(graph_path) as graph_file:
                    model.graph = json.load(graph_file)

                self.active_models[model_name] = model

    def list(self, active=None):
        return self.meta.copy()

    def add(self, model_name, n, tokenizer):
        # FIXME: Make sure model_name gets sanitized
        if model_name in self.meta:
            raise ValueError("There is already a model named %s" % (model_name,))

        self.active_models[model_name] = TextMarkov(n=n, tokenizer=tokenizer)
        self.meta[model_name] = {'n': n, 'tokenizer': tokenizer, 'active': True}

        self._save_graph(model_name)
        self._save_meta()

    def delete(self, model_name):
        del self.meta[model_name]
        self._save_meta()

        if model_name in self.active_models:
            del self.active_models[model_name]

        graph_path = self._get_graph_path(model_name)
        os.remove(graph_path)

    def random_text(self, model_name):
        return self.active_models[model_name].random_text()

    def train(self, model_name, texts):
        # FIXME: Race conditions!
        for text in texts:
            self.active_models[model_name].read_text(text)
        self._save_graph(model_name)

    def _get_graph_path(self, model_name):
        return os.path.join(self.graph_dir, model_name+'.json')

    def _save_meta(self):
        with open(self.meta_path, 'w') as meta_file:
            json.dump(self.meta, meta_file)

    def _save_graph(self, model_name):
        graph_path = self._get_graph_path(model_name)
        graph = self.active_models[model_name].graph
        with open(graph_path, 'w') as graph_file:
            json.dump(graph, graph_file)
