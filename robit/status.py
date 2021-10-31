STATUS_CHOICES = {
    'start': 'Starting',
    'halt': 'Halting',
    'stop': 'Stopped',
    'run': 'Running',
    'error': 'Error',
    'wait': 'Waiting',
}


class Status:
    def __init__(self, value: str = 'stop'):
        self.status = None
        self.set(value)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.verbose

    def set(self, value):
        if value in STATUS_CHOICES:
            self.status = value
        else:
            raise TypeError(f'{value} is and invalid status choice. Valid choices are {STATUS_CHOICES.keys()}')

    @property
    def verbose(self):
        return STATUS_CHOICES[self.status]