import uuid


class Id:
    def __init__(self) -> None:
        self.value = str(uuid.uuid4())

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.value

