import cv2

from FrameContainer import FrameContainer

THRESHOLDED_IMAGE = 1


def motion_detection_mask(_previous_frame, _current_frame):
    mask1 = cv2.cvtColor(_previous_frame, cv2.COLOR_RGB2GRAY)
    mask1 = cv2.GaussianBlur(mask1, (21, 21), 0)

    mask2 = cv2.cvtColor(_current_frame, cv2.COLOR_RGB2GRAY)
    mask2 = cv2.GaussianBlur(mask2, (21, 21), 0)

    diff = cv2.absdiff(mask1, mask2)
    threshold = cv2.threshold(diff, 21, 255, cv2.THRESH_BINARY)[THRESHOLDED_IMAGE]

    return threshold


def put_text_on_image(_frame, _text, _org=(50, 50)):
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = _org
    fontScale = 1
    color = (255, 0, 0)
    thickness = 2
    image_with_text = cv2.putText(_frame, _text, org, font,
                                  fontScale, color, thickness, cv2.LINE_AA)

    return image_with_text

def sum_from_period(_frameContainer: FrameContainer):
    th_len = len(_frameContainer.get_container_list())
    if th_len > 0:
        treshold_sum = sum(element.threshold for element in _frameContainer.get_container_list())
        return treshold_sum/th_len
    else:
        return 0

