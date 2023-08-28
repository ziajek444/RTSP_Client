from enum import Enum, unique


@unique
class Phase(Enum):
    CAPTURE = 1
    MOTION_DETECTION = 2
    BLUE = 3