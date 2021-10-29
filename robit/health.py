class Health:
    def __init__(self, max_count: int = 500):
        self.max_count: int = max_count
        self.percentage: float = 1.00
        self.positive_count: int = 0
        self.negative_count: int = 0

    def calculate(self):
        percentage_value = self.positive_count / (self.positive_count + self.negative_count)
        self.set_percentage(percentage_value)

    def add_negative(self, count: int = 1):
        self.negative_count += count

        if self.negative_count > self.max_count:
            self.negative_count = self.max_count

            if self.positive_count > 0:
                self.positive_count -= count

        self.calculate()

    def add_positive(self, count: int = 1):
        self.positive_count += count

        if self.positive_count > self.max_count:
            self.positive_count = self.max_count

            if self.negative_count > 0:
                self.negative_count -= count

        self.calculate()

    def set_percentage(self, value: float):
        if value > 100.0:
            self.percentage = 100.0
        elif value < 0.0:
            self.percentage = 0.0
        else:
            self.percentage = value

    def as_dict(self):
        return {
            'percentage': self.percentage,
        }