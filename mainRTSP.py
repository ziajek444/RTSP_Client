#!/usr/bin/env python -c

# Import OpenCV and threading packages
import cv2
import threading
import time


class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        self._start_time = time.perf_counter()

    def elapsed(self, expected_time):
        if self._start_time is None:
            return None
        elapsed_time = time.perf_counter() - self._start_time
        if expected_time > elapsed_time:
            return False
        else:
            return True


class FrameContainer:
    def __init__(self, size):
        self.size = size
        self.box = list()

    def add_frame(self, new_frame):
        self.box.append(new_frame)
        if len(self.box) > self.size:
            self.box.pop(0)

    def get_box(self):
        return self.box

    def clear_box(self):
        self.box.clear()


def motion_detection(frame, mog, kernel):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = mog.apply(gray)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    fgmask = cv2.dilate(fgmask, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    move_detected = False
    for contour in contours:
        move_detected = True
        # Ignore small contours
        if cv2.contourArea(contour) < 1000:
            continue
        # Draw bounding box around contour
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return move_detected, frame


# Define class for the camera thread.
class CamThread(threading.Thread):
    def __init__(self, previewname, camid):
        threading.Thread.__init__(self)
        self.previewname = previewname
        self.camid = camid

    def run(self):
        print("Starting " + self.previewname)
        previewcam(self.previewname, self.camid)

# Function to preview the camera.
def previewcam(previewname, camid):
    cv2.namedWindow(previewname)
    cam = cv2.VideoCapture(camid)
    resolutionWidth = None
    resolutionHeight = None
    if cam.isOpened():
        rval, frame = cam.read()
        resolution = (int(cam.get(3)), int(cam.get(4)),)
    else:
        rval = False

    mog = cv2.createBackgroundSubtractorMOG2()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    recorded = cv2.VideoWriter('testVideo.mp4',
                         cv2.VideoWriter_fourcc(*'MP4V'),
                         30.0, resolution)

    while rval:
        recorded.write(frame)
        frame = motion_detection(frame, mog, kernel)
        cv2.imshow(previewname, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # Press ESC to exit/close each window.
            break
    cam.release()  # Release the camera
    recorded.release()  # save the video
    cv2.destroyWindow(previewname)


class CustomCamThread(threading.Thread):
    def __init__(self, previewname, camid):
        threading.Thread.__init__(self)
        self.previewname = previewname
        self.camid = camid

    def run(self):
        print("Starting " + self.previewname)
        peek_until_move(self.previewname, self.camid)


def peek_until_move(previewname, camid):
    while True:
        print("Setup")
        # setup
        videosTaken = 0
        cv2.namedWindow(previewname)
        cam = cv2.VideoCapture(camid)
        resolution = (int(cam.get(3)), int(cam.get(4)),)
        mog = cv2.createBackgroundSubtractorMOG2()
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        frame_list = FrameContainer(300)
        key = None
        record_time = Timer()

        # constant preview
        while cam.isOpened():
            print("retry")
            rval, frame = cam.read()
            frame_list.add_frame(frame)
            move_detected, frame = motion_detection(frame, mog, kernel)
            cv2.imshow(previewname, frame)  ## preview

            if move_detected:
                print("save video")
                recorded = cv2.VideoWriter('testVideo_' + str(videosTaken) + '_.mp4',
                                           cv2.VideoWriter_fourcc(*'MP4V'),
                                           30.0, resolution)
                videosTaken += 1
                for singleframe in frame_list.box:
                    recorded.write(singleframe)
                frame_list.clear_box()
                record_time.start()
                while not record_time.elapsed(5.0):
                    rval, frame = cam.read()
                    recorded.write(frame)
                recorded.release()  # save the video


            key = cv2.waitKey(1)
            if key == 27:  # Press ESC to exit/close each window.
                break
        time.sleep(2)
        cam.release()  # Release the camera
        cv2.destroyWindow(previewname)




# Create different threads for each video stream, then start it.
thread1 = CustomCamThread("SpyCamera", 'https://admin:admin@192.168.0.38:4343/video')
#thread2 = CamThread("Front Door", 'rtsp://username:SuperSecurePassword@192.168.1.2/Streaming/Channels/202')
#thread3 = CamThread("Garage", 'rtsp://username:SuperSecurePassword@192.168.1.2/Streaming/Channels/302')
thread1.start()
#thread2.start()
#thread3.start()




#video speed
# get all frames
# record const time (example 60s)
# Sdelta = the littlest delta time between frames (example 0.019s)
# Ldelta = the longest time between frames (example 0.053s)
# Ddelta = digital delta = Ldelta / round_up(Ldelta/Sdelta) (example 0.053 / 3.0 = 0.01767 )
# frames per sec = amount of frames / 60
