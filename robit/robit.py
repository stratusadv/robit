from .clock import Clock


class Robit:
    def __init__(self, name):
        self.name = name
        self.clock = Clock()