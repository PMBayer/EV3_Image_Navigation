from enum import Enum


class Command(Enum):
    FORWARD = 'forward'
    BACKWARD = 'backward'
    RIGHT = 'right'
    LEFT = 'left'
    STOP = 'stop'
    END = 'end'
