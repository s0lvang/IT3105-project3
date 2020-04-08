from enum import Enum


class Direction(Enum):
    UP = (-1, 0)
    UPRIGHT = (-1, 1)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    DOWNLEFT = (1, -1)
    LEFT = (0, -1)
