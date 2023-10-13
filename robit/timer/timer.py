from robit.core.clock import Clock


class Timer:
    def __init__(
            self,
            duration_decimal_places: int = 2,
            duration_list_max: int = 20,
    ) -> None:
        self.start_time: float = 0.0

        self.duration_decimal_places = duration_decimal_places

        self.duration_list_max = duration_list_max
        self.duration_list = []

        self.average_duration = 0.0
        self.last_duration = 0.0
        self.shortest_duration = 0.0
        self.longest_duration = 0.0

        self.clock = Clock()

    def as_dict(self) -> dict:
        return {
            'average_duration': f'{self.average_duration:,.{self.duration_decimal_places}f}',
            'last_duration': f'{self.last_duration:,.{self.duration_decimal_places}f}',
            'shortest_duration': f'{self.shortest_duration:,.{self.duration_decimal_places}f}',
            'longest_duration': f'{self.longest_duration:,.{self.duration_decimal_places}f}',
        }

    def calculate_average_duration(self) -> None:
        total_duration = 0.0
        if len(self.duration_list) > 0:
            for duration in self.duration_list:
                total_duration += duration
            self.average_duration = total_duration / len(self.duration_list)

    def start(self) -> None:
        self.timer = self.clock.now_tz

    def stop(self) -> None:
        duration = (self.clock.now_tz - self.timer).total_seconds()

        self.last_duration = duration
        self.duration_list.insert(0, duration)

        if self.shortest_duration == 0 or duration < self.shortest_duration:
            self.shortest_duration = duration

        if self.longest_duration < duration:
            self.longest_duration = duration

        self.calculate_average_duration()
        self.trim_duration_list()

    def trim_duration_list(self) -> None:
        if len(self.duration_list) > self.duration_list_max:
            del self.duration_list[self.duration_list_max:]

