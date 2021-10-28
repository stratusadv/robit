class Health:
    def __init__(self, max_count: int = 500):
        self.max_count: int = max_count
        self.percentage: float = 100.00
        self.positive_count: int = 0
        self.negative_count: int = 0

    def calculate(self):
        self.percentage = self.positive_count / (self.positive_count + self.negative_count)
        if self.percentage > 100.0:
            self.percentage = 100.0
        if self.percentage < 0.0:
            self.percentage = 0.0

    def negative(self, count: int = 1):
        self.negative_count += count

        if self.negative_count > self.max_count:
            self.negative_count = self.max_count

            if self.positive_count > 0:
                self.positive_count -= count

        self.calculate()

    def positive(self, count: int = 1):
        self.positive_count += count

        if self.positive_count > self.max_count:
            self.positive_count = self.max_count

            if self.negative_count > 0:
                self.negative_count -= count

        self.calculate()


