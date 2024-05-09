class Health:
    def __init__(
            self,
            max_count: int = 100
    ) -> None:
        self.max_count: int = max_count
        self.percentage: float = 1.00
        self.average_reset: bool = False
        self.positive_count: int = 0
        self.negative_count: int = 0

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.percentage_verbose

    def average(self, value: float) -> None:
        if self.average_reset:
            self.percentage = value
            self.average_reset = False
        else:
            self.percentage = (self.percentage + value) / 2

    def calculate(self) -> None:
        percentage_value = self.positive_count / (self.positive_count + self.negative_count)
        self.set_percentage(percentage_value)

    def add_negative(self, count: int = 1) -> None:
        self.negative_count += count

        if self.negative_count > self.max_count:
            self.negative_count = self.max_count

            if self.positive_count > 0:
                self.positive_count -= count

        self.calculate()

    def add_positive(self, count: int = 1) -> None:
        self.positive_count += count

        if self.positive_count > self.max_count:
            self.positive_count = self.max_count

            if self.negative_count > 0:
                self.negative_count -= count

        self.calculate()

    @property
    def percentage_hundreds(self) -> float:
        return self.percentage * 100

    @property
    def percentage_verbose(self) -> str:
        return f'{self.percentage_hundreds:,.2f}'

    def reset(self) -> None:
        self.percentage = 0.0
        self.average_reset = True

    def set_percentage(self, value: float) -> None:
        if value > 1.0:
            self.percentage = 1.0
        elif value < 0.0:
            self.percentage = 0.0
        else:
            self.percentage = value

    def as_dict(self) -> dict:
        return {
            'max_count': self.max_count,
            'percentage': self.percentage,
            'positive_count': self.positive_count,
            'negative_count': self.negative_count,
        }
