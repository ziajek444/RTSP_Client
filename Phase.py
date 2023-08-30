from enum import Enum, unique


@unique
class Phase(Enum):
    CAPTURE = 1
    MOTION_DETECTION = 2
    DIFF_FRAMES = 3
    CONTAINER_A = 4
    RECORD = 5
    SAVE_CLIP = 6
    RESET = 7


