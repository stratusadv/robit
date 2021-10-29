import uuid


class Id:
    def __init__(self):
        self.value = str(uuid.uuid4())