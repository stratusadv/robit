class Counter:
    def __init__(self):
        self.total = 0

    def increase(self, count: int = 1):
        self.total += count

    def decrease(self, count: int = 1):
        self.total -= count

    def as_dict(self):
        return {
            'count': self.total
        }