from FrameObj import *


class FrameContainer:
    def __init__(self, size):
        self.size = size
        self.frame_obj_list = list()
        self.full = False

    def add_frame(self, frame_obj:FrameObj):
        if type(frame_obj) is not FrameObj:
            raise Exception("Wrong frame type")
        self.frame_obj_list.append(frame_obj)

        if len(self.frame_obj_list) > self.size:
            self.frame_obj_list.pop(0)
            self.full = True
            return True  # is full
        else:
            self.full = False
            return False  # is not full

    def get_container_list(self):
        return self.frame_obj_list

    def clear_container_list(self):
        self.full = False
        self.frame_obj_list.clear()
        while len(self.frame_obj_list) != 0:
            self.frame_obj_list.clear()

    def is_full(self):
        return self.full

    def __getitem__(self, key: int):
        return self.frame_obj_list[key]


