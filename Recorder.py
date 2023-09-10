import cv2
from datetime import date

from FileManagement import dir_exists, create_dir
from FrameContainer import FrameContainer
import time


class Recorder:
    def __init__(self, _prefix, _resolution):
        self.video_prefix_name = _prefix
        # fps
        self.resolution = _resolution
        self.frameContainersList = list()

    def add_frame_container(self, frameContainer: FrameContainer):
        self.frameContainersList.append(frameContainer)

    def build_clip(self, _directory="default"):
        fps = 0.0
        recorded = cv2.VideoWriter()
        try:
            for container in self.frameContainersList:
                fps += get_avg_fps(container)
            fps /= len(self.frameContainersList)
            if not dir_exists(_directory):
                create_dir(_directory)
            clip_fill_name_path = _directory + "/" + self.video_prefix_name + "_" + str(date.today()) + "_" + str(time.time()) + "_" + '.mp4'
            recorded = cv2.VideoWriter(clip_fill_name_path,
                                       cv2.VideoWriter_fourcc(*'MP4V'),
                                       fps, self.resolution)
            for container in self.frameContainersList:
                for frame in container:
                    recorded.write(frame.frame)
        except Exception as err:
            clip_fill_name_path = None
        finally:
            recorded.release()
            self.frameContainersList.clear()
        return clip_fill_name_path



def get_avg_fps(_frameContainer: FrameContainer):
    th_len = len(_frameContainer.get_container_list())
    if th_len > 0:
        deltaTime_sum = sum(element.deltaTime for element in _frameContainer.get_container_list())
        return th_len / deltaTime_sum
    else:
        return 0.016  # min val


