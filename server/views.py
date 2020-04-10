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
def add_model(manager, name, n, tokenizer):
    manager.add(name, n, tokenizer)


@router.register
def list_models(manager):
    return manager.list()


@router.register
def delete_model(manager, name):
    manager.delete(name)


@router.register
def train_model(manager, name, texts):
    manager.train(name, texts)


@router.register
def random_text(manager, name):
    model = server.models[name]
    return model.random_text()
