"""
main loop contains all features necessary to infinite recording loop
"""

from cam_features import *
from Phase import Phase



def main_loop(_rtsp_server: str, _source_name: str, _preview=False):
    # init
    dprint("init")
    phase = Phase.CAPTURE
    cam_data = CamData(_rtsp_server, _source_name)

    # preview
    PREVIEW = _preview
    if PREVIEW:
        cam_data.init_preview()

    # main body
    while True:
        if phase == Phase.CAPTURE:
            phase = cam_data.capture_phase()

        if phase == Phase.CONTAINER_A:
            phase = cam_data.container_A_phase()

        if phase == Phase.MOTION_DETECTION:
            phase = cam_data.motion_detection_phase()

        if phase == Phase.RECORD:
            phase = cam_data.record_phase()

        if phase == Phase.SAVE_CLIP:
            phase = cam_data.save_clip_phase()

        if phase == Phase.COMPRESS:
            phase = cam_data.compress_phase()

        if phase == Phase.RESET:
            phase = cam_data.reset_phase()

# ----------------------------
        if PREVIEW:
            cam_data.preview_phase()
# ----------------------------

    # close
    cam_data.clean_up()
    dprint("close")
    return "Error: Could not keep connection stable"


if __name__ == "__main__":
    rtsp_server = 'https://admin:admin@192.168.0.38:4343/video'
    fail = main_loop(rtsp_server, "Xiaomi")
    print(fail)
