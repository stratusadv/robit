from robit.status.enums import StatusChoiceEnum


class Status:
    def __init__(self, value: StatusChoiceEnum = StatusChoiceEnum.QUEUED):
        self._value = value

    def __repr__(self):
        return f'Status({self.value})'

    def __str__(self):
        return str(self.value)

    def error(self):
        self.value = StatusChoiceEnum.ERROR

    def halted(self):
        self.value = StatusChoiceEnum.HALT

    def queued(self):
        self.value = StatusChoiceEnum.QUEUED

    def running(self):
        self.value = StatusChoiceEnum.RUN

    def starting(self):
        self.value = StatusChoiceEnum.START

    def stopped(self):
        self.value = StatusChoiceEnum.STOP

    @property
    def value(self) -> str:
        return self._value.value

    @value.setter
    def value(self, value: StatusChoiceEnum):
        self._value = value

    def waiting(self):
        self.value = StatusChoiceEnum.WAIT


