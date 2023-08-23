'''
camera -> access to rtsp server (camera)


'''

import cv2
from preview import open_preview_window, play_preview, close_preview
from motionDetection import motion_detection_mask


# global setup
rtsp_server = 'https://admin:admin@192.168.0.38:4343/video'


def never_lost_conn(_rtsp_server: str):
    # init
    print("init")
    camera = get_valid_camera_when_ready(_rtsp_server)
    current_frame = None
    previous_frame = None

    ## motion detection
    mask_frame = None

    ## preview
    open_preview_window("preview_window")

    # main body of never_lost_conn()
    while True:
        print("main body")
        if camera_is_valid(camera):
            # req_neverLostConn
            previous_frame = current_frame
            current_frame = save_read_frame(camera)

            ## motion detection
            if not isinstance(current_frame, type(None)) and not isinstance(previous_frame, type(None)):
                mask_frame = motion_detection_mask(previous_frame, current_frame)

            ## preview
            if not isinstance(mask_frame, type(None)) and not isinstance(current_frame, type(None)) and not isinstance(previous_frame, type(None)):
                play_preview(mask_frame)
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
