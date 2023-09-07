'''
camera -> access to rtsp server (camera)


'''

import cv2

from CompressFile import compress_and_rm_files
from Phase import Phase
from Recorder import get_avg_fps, Recorder
from preview import open_preview_window, play_preview, close_preview
from motionDetection import motion_detection_mask, put_text_on_image, sum_from_period
from FrameContainer import FrameContainer
from FrameObj import FrameObj
import time

DEBUG = False           # If True, prints logs on console
CONTAINER_A_LEN = 10    # Default 100
CONTAINER_B_LEN = 20    # Default is 900


def never_lost_conn(_rtsp_server: str, _source_name: str, _preview=False):
    # init
    dprint("init")
    camera = get_valid_camera_when_ready(_rtsp_server)
    current_frame = None
    previous_frame = None
    resolution = (int(camera.get(3)), int(camera.get(4)),)
    phase = Phase.CAPTURE

    ## advanced use
    container_A = FrameContainer(CONTAINER_A_LEN)
    container_B = FrameContainer(CONTAINER_B_LEN)
    deltaTimer = time.time()

    ## recording
    recorder = Recorder(_source_name, resolution)

    ## motion detection
    frames_diff = None
    ACCURACY = 11000.0

    ## compress clip
    clip_full_path = None
    CLIPS_IN_ARCH = 4
    files_list_to_arch = list()

    ## preview
    PREVIEW = _preview
    if PREVIEW:
        open_preview_window(f"preview_window {_source_name}")

    # main body of never_lost_conn()
    while True:
        if phase == Phase.CAPTURE:
            dprint("CAPTURE")
            if camera_is_valid(camera):
                previous_frame = current_frame
                deltaTimer = time.time()
                current_frame = save_read_frame(camera)

                phase = Phase.CONTAINER_A
            else:
                dprint("error CAPTURE phase ")
                camera = get_valid_camera_when_ready(_rtsp_server)
                dprint("reconnected")

        if phase == Phase.CONTAINER_A:
            dprint("CONTAINER_A")
            if not isinstance(current_frame, type(None)) and not isinstance(previous_frame, type(None)):
                frames_diff = motion_detection_mask(previous_frame, current_frame)
                deltaTimer = time.time() - deltaTimer
                new_frame = FrameObj(current_frame, deltaTimer, frames_diff.sum())
                container_A.add_frame(new_frame)

                if container_A.is_full():
                    phase = Phase.MOTION_DETECTION
                else:
                    phase = Phase.CAPTURE
            else:
                phase = Phase.CAPTURE

        if phase == Phase.MOTION_DETECTION:
            dprint("MOTION_DETECTION")
            if sum_from_period(container_A) > ACCURACY:
                phase = Phase.RECORD
            else:
                phase = Phase.CAPTURE

        if phase == Phase.RECORD:
            dprint("RECORD")
            deltaTimer = time.time()
            while not container_B.is_full():
                current_frame = save_read_frame(camera)
                deltaTimer = time.time() - deltaTimer
                new_frame = FrameObj(current_frame, deltaTimer, 0)
                deltaTimer = time.time()
                container_B.add_frame(new_frame)
            phase = Phase.SAVE_CLIP

        if phase == Phase.SAVE_CLIP:
            dprint("SAVE_CLIP")
            recorder.add_frame_container(container_A)
            recorder.add_frame_container(container_B)
            clip_full_path = recorder.build_clip(_source_name + "_dir")
            if isinstance(clip_full_path, type(None)):
                phase = Phase.RESET
            else:
                files_list_to_arch.append(clip_full_path)
                if len(files_list_to_arch) >= CLIPS_IN_ARCH:
                    phase = Phase.COMPRESS
                else:
                    phase = Phase.RESET

        if phase == Phase.COMPRESS:
            arch_file_name = str(files_list_to_arch[0].replace('.', '_') + ".7z")
            compress_and_rm_files(files_list_to_arch, arch_file_name)
            files_list_to_arch.clear()
            assert len(files_list_to_arch) == 0
            phase = Phase.RESET

        if phase == Phase.RESET:
            dprint("RESET")
            container_B.clear_container_list()
            container_A.clear_container_list()
            #current_frame = None
            phase = Phase.CAPTURE

# ----------------------------

        if PREVIEW:
            if not isinstance(frames_diff, type(None)) and not isinstance(current_frame, type(None)):
                debug_frame = current_frame.copy()
                debug_frame = put_text_on_image(debug_frame, str(sum_from_period(container_A)))
                debug_frame = put_text_on_image(debug_frame, str(get_avg_fps(container_A)), (50, 100))
                play_preview(debug_frame)

# ----------------------------

    # release resources
    dprint("release")
    camera.release()
    ## preview
    close_preview()
    # close
    dprint("close")
    return "Error: Could not keep connection stable"


def get_valid_camera_when_ready(_rtsp_server: str):
    camera = cv2.VideoCapture()
    camera.setExceptionMode(True)
    while True:
        dprint("get_valid_camera_when_ready")
        try:
            camera.open(_rtsp_server)
            dprint("done")
            break
        except Exception as err:
            dprint("Exception catch : [", err, ']')

    dprint("camera connected: ", camera)
    return camera


def camera_is_valid(_camera):
    isCameraOpen = None
    try:
        if _camera.isOpened():
            isCameraOpen = True
        else:
            isCameraOpen = False
    except Exception as err:
        dprint("Exception catch : [", err, ']')
        isCameraOpen = False
    finally:
        return isCameraOpen


def save_read_frame(_camera):
    current_frame = None
    try:
        captured, current_frame = _camera.read()
    except Exception as err:
        dprint("Exception catch : [", err, ']')
        current_frame = None
        _camera.release()
    finally:
        return current_frame


def dprint(*args):
    global DEBUG
    if DEBUG:
        print(" ".join(map(str,args)))


if __name__ == "__main__":
    rtsp_server = 'https://admin:admin@192.168.0.38:4343/video'
    fail = never_lost_conn(rtsp_server, "Xiaomi")
    print(fail)
