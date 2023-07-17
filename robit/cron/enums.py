from enum import Enum


class CronFieldTypeEnum(Enum):
    EVERY = 'every'
    RANGE = 'range'
    STEP = 'step'
    LIST = 'list'
    SPECIFIC = 'specific'
