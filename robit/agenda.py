from robit.health import Health
from robit.id import Id


class Agenda:
    def __init__(self):
        self.id = Id()
        self.health = Health()