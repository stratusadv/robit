from datetime import datetime, timedelta

CREATED_DATE_FORMAT = '%b %d, %Y %I:%M%p'


class Clock:
    def __init__(self, timezone_utc_minus: int = 0, timer_duration_list_max: int = 10):
        self.timezone_utc_minus = timezone_utc_minus

        self.created_utc = datetime.utcnow()
        self.created_tz = datetime.utcnow() - timedelta(hours=timezone_utc_minus)

        self.timer_duration_list_max = timer_duration_list_max
        self.timer_duration_list = []
        self.timer_average_duration = 0.0
        self.timer_last_duration = 0.0
        self.timer_shortest_duration = 0.0
        self.timer_longest_duration = 0.0
        self.timer = None

    def as_dict(self):
        return {
            'created': self.created_tz_verbose,
            'timer_last_duration': f'{self.timer_last_duration:.2f}',
            'timer_average_duration': f'{self.timer_average_duration:.2f}',
            'timer_shortest_duration': f'{self.timer_shortest_duration:.2f}',
            'timer_longest_duration': f'{self.timer_longest_duration:.2f}',
        }

    def calculate_timer_average_duration(self):
        timer_total_duration = 0.0
        if len(self.timer_duration_list) > 0:
            for timer_duration in self.timer_duration_list:
                timer_total_duration += timer_duration
            self.timer_average_duration = timer_total_duration / len(self.timer_duration_list)

    @property
    def created_utc_verbose(self):
        return self.created_utc.strftime(CREATED_DATE_FORMAT)

    @property
    def created_tz_verbose(self):
        return self.created_tz.strftime(CREATED_DATE_FORMAT)

    def start_timer(self):
        self.timer = datetime.utcnow()

    def stop_timer(self):
        duration = (datetime.utcnow() - self.timer).total_seconds()

        self.timer_last_duration = duration
        self.timer_duration_list.insert(0, duration)

        if self.timer_shortest_duration == 0 or duration < self.timer_shortest_duration:
            self.timer_shortest_duration = duration

        if self.timer_longest_duration < duration:
            self.timer_longest_duration = duration

        self.calculate_timer_average_duration()
        self.trim_timer_duration_list()

    def trim_timer_duration_list(self):
        if len(self.timer_duration_list) > self.timer_duration_list_max:
            del self.timer_duration_list[self.timer_duration_list_max:]


