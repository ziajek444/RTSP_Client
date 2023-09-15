import cv2
from datetime import date
from FileManagement import dir_exists, create_dir
from FrameContainer import FrameContainer
import time
from simple_logs import log_debug, log_error

TO_CONSOLE = False       # Default False


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
            clip_fill_name_path = _directory + "/" + self.video_prefix_name + "_[" + str(time.time())[-4:] + "]_fps[" + str(fps)[0:5] + ']_[' + str(date.today())[-5:] + '].mp4'
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

    def build_clip_with_duration_b(self, _con_b_clip_duration: float, _directory="default", _limit_min: float = 1.0, _limit_max: float = 1024.0):
        recorded = cv2.VideoWriter()
        try:
            biggest_container_len = 0
            for container in self.frameContainersList:
                con_len = len(container.get_container_list())
                if con_len > biggest_container_len:
                    biggest_container_len = con_len
            assert biggest_container_len > 0
            assert _con_b_clip_duration > 0
            fps = clamp(biggest_container_len / _con_b_clip_duration, _limit_min, _limit_max)
            log_debug(f"fps: {fps}, frames: {biggest_container_len}, duration: {_con_b_clip_duration} ", to_console=TO_CONSOLE)

            if not dir_exists(_directory):
                create_dir(_directory)
            clip_fill_name_path = _directory + "/" + self.video_prefix_name + "_[" + \
                                  str(int(time.time()))[-6:] + "]_fps[" + str(fps)[0:5] + ']_[' + \
                                  str(date.today())[-5:] + '].mp4'
            recorded = cv2.VideoWriter(clip_fill_name_path,
                                       cv2.VideoWriter_fourcc(*'MP4V'),
                                       fps, self.resolution)
            for container in self.frameContainersList:
                for frame in container:
                    recorded.write(frame.frame)
            log_debug(f"recorded: {recorded} ", to_console=TO_CONSOLE)
        except Exception as err:
            log_error(f"build_clip_with_duration_b, Exception {str(err)}", to_console=TO_CONSOLE)
            clip_fill_name_path = None
        finally:
            recorded.release()
            self.frameContainersList.clear()
        log_debug(f"clip name: {clip_fill_name_path} ", to_console=TO_CONSOLE)
        return clip_fill_name_path


def get_avg_fps(_frameContainer: FrameContainer, _limit_min: float = 1.0, _limit_max: float = 1024.0):
    th_len = len(_frameContainer.get_container_list())
    if th_len > 0:
        deltaTime_sum = sum(element.deltaTime for element in _frameContainer.get_container_list())
        ret_fps = clamp(th_len / deltaTime_sum, _limit_min, _limit_max)
        return ret_fps
    else:
        return 0.0


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)
