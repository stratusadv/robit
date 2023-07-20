from enum import Enum


class StatusChoiceEnum(Enum):
    START = 'Start'
    HALT = 'Halt'
    STOP = 'Stopped'
    RUN = 'Running'
    ERROR = 'Error'
    WAIT = 'Waiting'
    QUEUED = 'Queued'


