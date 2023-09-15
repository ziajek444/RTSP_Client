import cv2
from FileManagement import extract_path_without_extension
from Phase import Phase
import time
from motionDetection import motion_detection_mask, sum_from_period, put_text_on_image
from FrameObj import FrameObj
from FrameContainer import FrameContainer
from Recorder import Recorder, get_avg_fps
from CompressFile import compress_and_rm_files
from preview import play_preview, close_preview, open_preview_window
from Cloud import upload_files
import threading
from simple_logs import log_debug, log_info, log_error

CONTAINER_A_LEN = 30    # Default 100
CONTAINER_B_LEN = 600    # Default is 900
TO_CONSOLE = False       # Default False


def get_valid_camera_when_ready(_rtsp_server: str):
    camera = cv2.VideoCapture()
    camera.setExceptionMode(True)
    while True:
        log_debug("get_valid_camera_when_ready", to_console=TO_CONSOLE)
        try:
            camera.open(_rtsp_server)
            log_info("done", to_console=TO_CONSOLE)
            break
        except Exception as err:
            log_info("Exception catch : [", err, ']', to_console=TO_CONSOLE)

    log_info("camera connected: ", camera, to_console=TO_CONSOLE)
    return camera


def camera_is_valid(_camera):
    isCameraOpen = None
    try:
        if _camera.isOpened():
            isCameraOpen = True
        else:
            isCameraOpen = False
    except Exception as err:
        log_error("Exception catch : [", err, ']', to_console=TO_CONSOLE)
        isCameraOpen = False
    finally:
        return isCameraOpen


def save_read_frame(_camera):
    current_frame = None
    try:
        captured, current_frame = _camera.read()
    except Exception as err:
        log_error("Exception catch : [", err, ']', to_console=TO_CONSOLE)
        current_frame = None
        _camera.release()
    finally:
        return current_frame


class CamData:
    def __init__(self, _rtsp_server: str, _source_name: str):
        global CONTAINER_A_LEN, CONTAINER_B_LEN

        ## camera
        self.rtsp_server = _rtsp_server
        self.source_name = _source_name
        self.camera = get_valid_camera_when_ready(_rtsp_server)
        self.current_frame = None
        self.previous_frame = None
        self.resolution = (int(self.camera.get(3)), int(self.camera.get(4)),)

        ## advanced use
        self.container_A = FrameContainer(CONTAINER_A_LEN)
        self.container_B = FrameContainer(CONTAINER_B_LEN)
        self.deltaTimer = time.time()

        ## recording
        self.recorder = Recorder(_source_name, self.resolution)
        self.con_B_clip_duration = None

        ## motion detection
        self.frames_diff = None
        self.ACCURACY = 5000.0

        ## compress clip
        self.clip_full_path = None
        self.CLIPS_IN_ARCH = 4
        self.files_list_to_arch = list()
        self.arch_file_name = None

        ## cloud data
        self.dir_id = None
        self.files_to_upload = list()

    def capture_phase(self):
        log_debug("CAPTURE", to_console=TO_CONSOLE)
        new_phase = None
        if camera_is_valid(self.camera):
            self.previous_frame = self.current_frame
            self.deltaTimer = time.time()
            self.current_frame = save_read_frame(self.camera)
            new_phase = Phase.CONTAINER_A
        else:
            log_error("error CAPTURE phase ", to_console=TO_CONSOLE)
            self.camera = get_valid_camera_when_ready(self.rtsp_server)
            log_info("reconnected", to_console=TO_CONSOLE)
            new_phase = Phase.CAPTURE
        return new_phase

    def container_A_phase(self):
        log_debug("CONTAINER_A", to_console=TO_CONSOLE)
        new_phase = None
        if not isinstance(self.current_frame, type(None)) and not isinstance(self.previous_frame, type(None)):
            self.frames_diff = motion_detection_mask(self.previous_frame, self.current_frame)
            self.deltaTimer = time.time() - self.deltaTimer
            new_frame = FrameObj(self.current_frame, self.deltaTimer, self.frames_diff.sum())
            self.container_A.add_frame(new_frame)
            if self.container_A.is_full():
                new_phase = Phase.MOTION_DETECTION
            else:
                new_phase = Phase.CAPTURE
        else:
            new_phase = Phase.CAPTURE
        return new_phase

    def motion_detection_phase(self):
        log_debug("MOTION_DETECTION", to_console=TO_CONSOLE)
        new_phase = None
        if sum_from_period(self.container_A) > self.ACCURACY:
            new_phase = Phase.RECORD
        else:
            new_phase = Phase.CAPTURE
        return new_phase

    def record_phase(self):
        log_debug("RECORD", to_console=TO_CONSOLE)
        new_phase = None
        self.deltaTimer = time.time()
        self.con_B_clip_duration = time.time()  # feature: time elapsed during rec only container_B
        while not self.container_B.is_full():
            self.current_frame = save_read_frame(self.camera)
            self.deltaTimer = time.time() - self.deltaTimer
            new_frame = FrameObj(self.current_frame, self.deltaTimer, 0)
            self.deltaTimer = time.time()
            self.container_B.add_frame(new_frame)
        start_time = self.con_B_clip_duration
        stop_time = time.time()
        diff_time = stop_time - self.con_B_clip_duration
        self.con_B_clip_duration = diff_time
        log_debug(f"start time: {start_time} - fin time {stop_time} - diff time {diff_time} ", to_console=TO_CONSOLE)
        new_phase = Phase.SAVE_CLIP
        return new_phase

    def save_clip_phase(self):
        log_debug("SAVE_CLIP", to_console=TO_CONSOLE)
        new_phase = None
        self.recorder.add_frame_container(self.container_A)
        self.recorder.add_frame_container(self.container_B)
        #clip_full_path = self.recorder.build_clip(self.source_name + "_dir")
        # feature: time elapsed during rec only container_B
        clip_full_path = self.recorder.build_clip_with_duration_b(self.con_B_clip_duration, self.source_name + "_dir",
                                                                  19.99, 61.0)
        if isinstance(clip_full_path, type(None)):
            new_phase = Phase.RESET
        else:
            self.files_list_to_arch.append(clip_full_path)
            if len(self.files_list_to_arch) >= self.CLIPS_IN_ARCH:
                new_phase = Phase.COMPRESS
            else:
                new_phase = Phase.RESET
        return new_phase

    def compress_phase(self, _compress_disabled=False):
        log_debug("COMPRESS", to_console=TO_CONSOLE)
        new_phase = None
        self.arch_file_name = str(extract_path_without_extension(self.files_list_to_arch[0])) + ".7z"
        if not _compress_disabled:
            compress_and_rm_files(self.files_list_to_arch, self.arch_file_name)
            if self.dir_id:
                self.files_to_upload = [self.arch_file_name].copy()
            else:
                self.files_to_upload = list()
        else:
            if self.dir_id:
                self.files_to_upload = self.files_list_to_arch.copy()
            else:
                self.files_to_upload = list()

        self.files_list_to_arch.clear()
        assert len(self.files_list_to_arch) == 0
        new_phase = Phase.UPLOAD
        return new_phase

    def upload_phase(self):
        log_debug("UPLOAD", to_console=TO_CONSOLE)
        new_phase = None
        if len(self.files_to_upload) > 0:
            upload_th = threading.Thread(name='upload_th', target=upload_files,
                                         args=(self.files_to_upload, self.dir_id,))
            upload_th.start()
        new_phase = Phase.RESET
        return new_phase

    def reset_phase(self):
        log_debug("RESET", to_console=TO_CONSOLE)
        new_phase = None
        self.container_B.clear_container_list()
        self.container_A.clear_container_list()
        new_phase = Phase.CAPTURE
        return new_phase

    def preview_phase(self):
        log_debug("PREVIEW", to_console=TO_CONSOLE)
        if not isinstance(self.frames_diff, type(None)) and not isinstance(self.current_frame, type(None)):
            debug_frame = self.current_frame.copy()
            debug_frame = put_text_on_image(debug_frame, str(sum_from_period(self.container_A)))
            debug_frame = put_text_on_image(debug_frame, str(get_avg_fps(self.container_A)), (50, 100))
            play_preview(debug_frame)

    def set_dir_id(self, _dir_id: str):
        self.dir_id = _dir_id

    def init_preview(self):
        open_preview_window(f"preview_window {self.source_name}")

    def clean_up(self):
        log_debug("CLEAN_UP", to_console=TO_CONSOLE)
        self.camera.release()
        close_preview()
