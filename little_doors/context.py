class Context(object):
    __contexts = []

    def __init__(self, game, window):
        self.game = game
        self.window = window

    @classmethod
    def current(cls):
        return cls.__contexts[len(cls.__contexts) - 1] if cls.__contexts else None

    def __enter__(self):
        Context.__contexts.append(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if Context.__contexts:
            Context.__contexts.pop()
