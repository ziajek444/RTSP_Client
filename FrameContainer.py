from FrameObj import *


class FrameContainer:
    def __init__(self, size):
        self.size = size
        self.frame_box = list()
        self.delta_time_list = list()
        self.full = False

    def add_frame(self, frame_obj:FrameObj):
        if type(frame_obj) is not FrameObj:
            raise Exception("Wrong frame type")
        self.frame_box.append(frame_obj.frame)
        self.delta_time_list.append(frame_obj.catch_time_ms)
        if len(self.frame_box) != len(self.delta_time_list):
            raise Exception("Something gone wrong", len(self.frame_box), len(self.delta_time_list))

        if len(self.frame_box) > self.size:
            self.frame_box.pop(0)
            self.delta_time_list.pop(0)
            self.full = True
            return True  # is full
        else:
            self.full = False
            return False  # is not full

    def get_box(self):
        return self.frame_box

    def clear_box(self):
        self.full = False
        self.frame_box.clear()

    def get_delta_time(self):
        return len(self.delta_time_list)/sum(self.delta_time_list)  # 1/sum/len = len/sum

    def is_full(self):
        return self.full


