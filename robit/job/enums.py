from enum import Enum


class JobExecutionType(str, Enum):
    THREAD = 'thread'
    PROCESS = 'process'

    def __str__(self):
        return self.value.capitalize()


class JobResultType(str, Enum):
    COMPLETED = 'completed'
    ERRORED = 'errored'

    def __str__(self):
        return self.value.capitalize()


class JobStatus(str, Enum):
    START = 'start'
    HALT = 'halting'
    STOP = 'stopped'
    RUN = 'running'
    RUN_NOW = 'running now'
    RETRY = 'retrying'
    ERROR = 'error'
    WAIT = 'waiting'
    QUEUED = 'queued'
    PAUSED = 'paused'

    def __str__(self):
        return self.value.capitalize()
