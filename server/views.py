import os
from models.text_markov import TextMarkov
MODELS_PATH = '.data/models'


class Router:
    def __init__(self):
        self.views = {}

    def register(self, command_function, command=None):
        if command is None:
            command = command_function.__name__
        self.views[command] = command_function


router = Router()


@router.register
def add_model(server, name, n, tokenizer):
    if name in server.models:
        raise ValueError("There is already a model named: %s" % (name,))

    server.config['models'][name] = {
        'active': True,
        'n': n,
        'tokenizer': tokenizer,
        'path': os.path.join(MODELS_PATH, name)
    }

    server.models[name] = TextMarkov(n, tokenizer)

    server.save_graph(name)
    server.save_config()


@router.register
def list_models(server):
    return server.config['models']


@router.register
def train_model(server, name, texts):
    model = server.models[name]

    for text in texts:
        model.read_text(text)

    server.save_graph(name)


@router.register
def random_sequence(server, name):
    model = server.models[name]
    return model.random_sequence()


@router.register
def random_text(server, name):
    model = server.models[name]
    return model.random_text()
