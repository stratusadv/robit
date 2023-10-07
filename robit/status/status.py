from robit.status.enums import StatusChoiceEnum


class Status:
    def __init__(self, value: StatusChoiceEnum = StatusChoiceEnum.QUEUED) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f'Status({self.value})'

    def __str__(self) -> str:
        return str(self.value)

    def error(self) -> None:
        self.value = StatusChoiceEnum.ERROR

    def halted(self) -> None:
        self.value = StatusChoiceEnum.HALT

    def queued(self) -> None:
        self.value = StatusChoiceEnum.QUEUED

    def running(self) -> None:
        self.value = StatusChoiceEnum.RUN

    def starting(self) -> None:
        self.value = StatusChoiceEnum.START

    def stopped(self) -> None:
        self.value = StatusChoiceEnum.STOP

    @property
    def value(self) -> str:
        return self._value.value

    @value.setter
    def value(self, value: StatusChoiceEnum) -> None:
        self._value = value

    def waiting(self) -> None:
        self.value = StatusChoiceEnum.WAIT


