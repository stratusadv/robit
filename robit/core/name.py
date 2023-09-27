from dataclasses import dataclass


@dataclass()
class Name:
    name: str

    def __str__(self) -> str:
        return self.name
