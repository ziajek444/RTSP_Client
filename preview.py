import cv2


# global data
PREVIEW_WINDOW_NAME = None


def set_preview_resolution(_camera):
    preview_resolution = (int(_camera.get(3)), int(_camera.get(4)),)
    return preview_resolution


def open_preview_window(_previewname):
    global PREVIEW_WINDOW_NAME
    PREVIEW_WINDOW_NAME = _previewname
    cv2.namedWindow(PREVIEW_WINDOW_NAME)


def play_preview(_frame):
    cv2.imshow(PREVIEW_WINDOW_NAME, _frame)
    cv2.waitKey(1)


def close_preview():
    cv2.destroyAllWindows()
