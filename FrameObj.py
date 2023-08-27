class FrameObj:
    def __init__(self, frame, deltaTime, treshold):
        self.deltaTime = deltaTime  # time diff from previous frame
        self.frame = frame
        self.threshold = treshold   # pixel diff from previous frame
