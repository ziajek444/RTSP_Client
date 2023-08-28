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
    deltaTimer = time.time_ns()

    ## recording
    RecordingInProgress = False
    recorder = Recorder("test", resolution)

    ## motion detection
    mask_frame = None

    ## preview
    open_preview_window("preview_window")

    ## debug data on image


    # main body of never_lost_conn()
    while True:
        print("main body")
        if camera_is_valid(camera):
            # Capture Phase
            if phase == Phase.CAPTURE:
                previous_frame = current_frame
                current_frame = save_read_frame(camera)
                if not isinstance(previous_frame, type(None)):
                    phase = Phase.MOTION_DETECTION
                else:
                    print("First frame should be None")

            ## motion detection
            if not isinstance(current_frame, type(None)) and not isinstance(previous_frame, type(None)) and not RecordingInProgress:
                mask_frame = motion_detection_mask(previous_frame, current_frame)
                if sum_from_period(container_A) > 10000.0:
                    RecordingInProgress = True

            ## advenced use
            if not isinstance(mask_frame, type(None)):
                if not RecordingInProgress:
                    deltaTimer = time.time_ns() - deltaTimer
                    new_frame = FrameObj(current_frame, deltaTimer, mask_frame.sum())
                    container_A.add_frame(new_frame)
                    deltaTimer = time.time_ns()
                else:
                    deltaTimer = time.time_ns() - deltaTimer
                    new_frame = FrameObj(current_frame, deltaTimer, mask_frame.sum())
                    container_B.add_frame(new_frame)
                    deltaTimer = time.time_ns()
                    if container_B.is_full():
                        RecordingInProgress = False
                        recorder.add_frame_container(container_A)
                        recorder.add_frame_container(container_B)
                        recorder.build_clip()
                        container_B.clear_container_list()
                        container_A.clear_container_list()
                        time.sleep(5.0)
                        deltaTimer = time.time_ns()


            ## debug data on image
            if not isinstance(mask_frame, type(None)):
                if isinstance(current_frame, type(None)):
                    raise Exception("WTF??")
                debug_frame = current_frame.copy()
                debug_frame = put_text_on_image(debug_frame, str(sum_from_period(container_A)))
                debug_frame = put_text_on_image(debug_frame, str(get_avg_fps(container_A)), (50, 100))

            ## preview
            if not isinstance(mask_frame, type(None)):
                play_preview(debug_frame)
                print(">>>", mask_frame.sum())
        else:
            # req_neverLostConn
            print("error #nlc_01 ")
            camera = get_valid_camera_when_ready(_rtsp_server)
            print("reconnected")

    # release resources
    print("release")
    camera.release()

    ## preview
    close_preview()

    # close
    print("close")
    return "Error: Could not keep connection stable"


def get_valid_camera_when_ready(_rtsp_server: str):
    print("get_valid_camera_when_ready")
    camera = cv2.VideoCapture()
    camera.setExceptionMode(True)
    while True:
        print("try to connect with camera")
        try:
            camera.open(_rtsp_server)
            print("done")
            break
        except Exception as err:
            print("Exception catch : [", err, ']')

    print("camera connected: ", camera)
    return camera


def camera_is_valid(_camera):
    print("camera_is_valid")
    isCameraOpen = None
    try:
        if _camera.isOpened():
            isCameraOpen = True
        else:
            isCameraOpen = False
    except Exception as err:
        print("Exception catch : [", err, ']')
        print("camera_is_valid error #1")
        isCameraOpen = False
    finally:
        print("camera_is_valid ret:", isCameraOpen)
        return isCameraOpen


def save_read_frame(_camera):
    print("save_read_frame")
    current_frame = None
    try:
        captured, current_frame = _camera.read()
    except Exception as err:
        print("Exception catch : [", err, ']')
        print("save_read_frame error #1")
        current_frame = None
        _camera.release()
    finally:
        print("save_read_frame ret:", type(current_frame))
        return current_frame


fail = never_lost_conn(rtsp_server)
print(fail)
