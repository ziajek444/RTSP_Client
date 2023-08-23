import cv2


THRESHOLDED_IMAGE = 1


def motion_detection_mask(_previous_frame, _current_frame):
    mask1 = cv2.cvtColor(_previous_frame, cv2.COLOR_RGB2GRAY)
    mask1 = cv2.GaussianBlur(mask1, (11, 11), 0)

    mask2 = cv2.cvtColor(_current_frame, cv2.COLOR_RGB2GRAY)
    mask2 = cv2.GaussianBlur(mask2, (11, 11), 0)

    diff = cv2.absdiff(mask1, mask2)
    threshold = cv2.threshold(diff, 127, 255, cv2.THRESH_BINARY)[THRESHOLDED_IMAGE]

    return threshold
