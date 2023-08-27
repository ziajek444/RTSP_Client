import cv2
from datetime import date
from FrameContainer import FrameContainer


class Recorder:
    def __init__(self, _prefix, _resolution, start_id=1):
        self.video_prefix_name = _prefix
        # fps
        self.resolution = _resolution
        self.frameContainersList = list()
        self.ID = start_id

    def add_frame_container(self, frameContainer: FrameContainer):
        self.frameContainersList.append(frameContainer)

    def build_clip(self):
        fps = 0.0
        for container in self.frameContainersList:
            fps += get_avg_fps(container)
        fps /= len(self.frameContainersList)
        recorded = cv2.VideoWriter(self.video_prefix_name + "_" + str(date.today()) + "_" + str(self.ID) + '.mp4',
                                   cv2.VideoWriter_fourcc(*'MP4V'),
                                   fps, self.resolution)
        self.ID += 1
        for container in self.frameContainersList:
            for frame in container:
                recorded.write(frame.frame)

        recorded.release()
        self.frameContainersList.clear()



def get_avg_fps(_frameContainer: FrameContainer):
    th_len = len(_frameContainer.get_container_list())
    if th_len > 0:
        deltaTime_sum = sum(element.deltaTime for element in _frameContainer.get_container_list())
        return (deltaTime_sum / th_len)/1000000.0   # for nanosec
    else:
        return 0.0


