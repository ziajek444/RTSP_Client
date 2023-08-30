'''
camera -> access to rtsp server (camera)


'''

import cv2

from Phase import Phase
from Recorder import get_avg_fps, Recorder
from preview import open_preview_window, play_preview, close_preview
from motionDetection import motion_detection_mask, put_text_on_image, sum_from_period
from FrameContainer import FrameContainer
from FrameObj import FrameObj
import time

# global setup
rtsp_server = 'https://admin:admin@192.168.0.38:4343/video'


def never_lost_conn(_rtsp_server: str):
    # init
    print("init")
    camera = get_valid_camera_when_ready(_rtsp_server)
    current_frame = None
    previous_frame = None
    resolution = (int(camera.get(3)), int(camera.get(4)),)
    phase = Phase.CAPTURE

    ## advanced use
    container_A = FrameContainer(100)
    container_B = FrameContainer(200)
    deltaTimer = time.time()

    ## recording
    recorder = Recorder("test", resolution)

    ## motion detection
    frames_diff = None

    ## preview
    open_preview_window("preview_window")


    # main body of never_lost_conn()
    while True:
        if phase == Phase.CAPTURE:
            print("CAPTURE")
            if camera_is_valid(camera):
                previous_frame = current_frame
                deltaTimer = time.time()
                current_frame = save_read_frame(camera)

                phase = Phase.CONTAINER_A
            else:
                print("error CAPTURE phase ")
                camera = get_valid_camera_when_ready(_rtsp_server)
                print("reconnected")

        if phase == Phase.CONTAINER_A:
            print("CONTAINER_A")
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
            print("MOTION_DETECTION")
            if sum_from_period(container_A) > 15000.0:
                phase = Phase.RECORD
            else:
                phase = Phase.CAPTURE

        if phase == Phase.RECORD:
            print("RECORD")
            deltaTimer = time.time()
            while not container_B.is_full():
                current_frame = save_read_frame(camera)
                deltaTimer = time.time() - deltaTimer
                new_frame = FrameObj(current_frame, deltaTimer, 0)
                deltaTimer = time.time()
                container_B.add_frame(new_frame)
            phase = Phase.SAVE_CLIP

        if phase == Phase.SAVE_CLIP:
            print("SAVE_CLIP")
            recorder.add_frame_container(container_A)
            recorder.add_frame_container(container_B)
            recorder.build_clip()
            phase = Phase.RESET

        if phase == Phase.RESET:
            print("RESET")
            container_B.clear_container_list()
            container_A.clear_container_list()
            #current_frame = None
            phase = Phase.CAPTURE

            #// ----------------------------

        ## debug data on image
        if not isinstance(frames_diff, type(None)):
            if isinstance(current_frame, type(None)):
                raise Exception("WTF??")
            debug_frame = current_frame.copy()
            debug_frame = put_text_on_image(debug_frame, str(sum_from_period(container_A)))
            debug_frame = put_text_on_image(debug_frame, str(get_avg_fps(container_A)), (50, 100))

        ## preview
        if not isinstance(frames_diff, type(None)):
            play_preview(debug_frame)


    # release resources
    print("release")
    camera.release()
    ## preview
    close_preview()
    # close
    print("close")
    return "Error: Could not keep connection stable"


def get_valid_camera_when_ready(_rtsp_server: str):
    camera = cv2.VideoCapture()
    camera.setExceptionMode(True)
    while True:
        print("get_valid_camera_when_ready")
        try:
            camera.open(_rtsp_server)
            print("done")
            break
        except Exception as err:
            print("Exception catch : [", err, ']')

    print("camera connected: ", camera)
    return camera


def camera_is_valid(_camera):
    isCameraOpen = None
    try:
        if _camera.isOpened():
            isCameraOpen = True
        else:
            isCameraOpen = False
    except Exception as err:
        print("Exception catch : [", err, ']')
        isCameraOpen = False
    finally:
        return isCameraOpen


def save_read_frame(_camera):
    current_frame = None
    try:
        captured, current_frame = _camera.read()
    except Exception as err:
        print("Exception catch : [", err, ']')
        current_frame = None
        _camera.release()
    finally:
        return current_frame


fail = never_lost_conn(rtsp_server)
print(fail)
