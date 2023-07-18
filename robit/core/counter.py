from dataclasses import dataclass


@dataclass()
class Counter:
    total: int = 0

    def __str__(self):
        return str(self.total)

    def __repr__(self):
        return self.total

    def increase(self, count: int = 1) -> None:
        self.total += count

    def decrease(self, count: int = 1) -> None:
        self.total -= count

    def as_dict(self) -> dict:
        return {
            'count': self.total
        }
