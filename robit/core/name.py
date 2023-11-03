from dataclasses import dataclass


@dataclass()
class Name:
    name: str

    def to_slug(self):
        pass

    def to_snake(self):
        pass

    def __str__(self) -> str:
        return self.name
