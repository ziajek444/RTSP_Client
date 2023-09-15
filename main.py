"""
main loop contains all features necessary to infinite recording loop
"""
from FileManagement import get_all_files_in_dir, get_last_modification, rm_7z_files_older_than_s, \
    daemon_remove_files_older_than_10min
from cam_features import *
from Phase import Phase
from setup_data import setup_json_data
from simple_logs import *
import threading

TO_CONSOLE = False       # Default True


def main_loop(_rtsp_server: str, _source_name: str, _preview=False):
    # init
    log_info("init", to_console=TO_CONSOLE)
    phase = Phase.CAPTURE
    setup_data = setup_json_data()

    # cam main obj
    cam_data = CamData(_rtsp_server, _source_name)
    cam_data.set_dir_id(setup_data["parent_directory"])

    # Files Garbage Collector
    full_clip_dir = os.getcwd() + '/' + _source_name + "_dir/"
    files_garbage_collector = threading.Thread(target=daemon_remove_files_older_than_10min, args=(full_clip_dir,))
    files_garbage_collector.start()

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
            phase = cam_data.compress_phase(_compress_disabled=False)

        if phase == Phase.UPLOAD:
            phase = cam_data.upload_phase()

        if phase == Phase.RESET:
            phase = cam_data.reset_phase()

# ----------------------------
        if PREVIEW:
            cam_data.preview_phase()
# ----------------------------

    # close
    cam_data.clean_up()
    log_critical("Error: Could not keep connection stable", to_console=TO_CONSOLE)
    return "Error: Could not keep connection stable"


if __name__ == "__main__":
    rtsp_server = 'https://admin:admin@192.168.0.120:4343/video'
    fail = main_loop(rtsp_server, "Piateczek")
    log_critical(fail, to_console=TO_CONSOLE)
