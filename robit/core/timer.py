class Timer:
    def __init__(self):
        self.start_time: float = 0.0
        self.stop_time: float = 0.0

        self.average: float = 0.0
        self.current: float = 0.0
        self.fastest: float = 0.0
        self.previous: float = 0.0
        self.slowest: float = 0.0

    def start(self):
        pass

    def stop(self):
        pass

    def as_dict(self):
        return {
            'average': self.average,
            'current': self.current,
            'fastest': self.fastest,
            'previous': self.previous,
            'slowest': self.slowest,
        }
