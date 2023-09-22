from dataclasses import dataclass


@dataclass
class Counter:
    total: int = 0

    def __str__(self) -> str:
        return str(self.total)

    def __repr__(self) -> int:
        return self.total

    def as_dict(self) -> dict:
        return {
            'count': self.total
        }

    def decrease(self, count: int = 1) -> None:
        self.total -= count

    def increase(self, count: int = 1) -> None:
        self.total += count
