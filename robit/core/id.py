import uuid


class Id:
    def __init__(self):
        self.value = str(uuid.uuid4())

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.value

