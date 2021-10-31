class Name:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name
