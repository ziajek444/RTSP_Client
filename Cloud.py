'''
API for checking space on cloud drive (like google drive).
API for pushing files into cloud drive.
Idea:
    Thread working at every n minutes and checking if there are any files to push
'''

# TODO
def push_file(path_to_file: str):
    # if file exists get size of file in bytes => file_size
    if enough_cloud_space_left(file_size):
        # push file into cloud drive
        if not is_file_exists_on_drive(file_name):
            # => False
        else:
            # => True
    else:
        # => False

# TODO
def enough_cloud_space_left(req_space: int):
    # get cloud left space
    # compare required and left spaces
    # if req < left => True
    # else => False

# TODO
def is_file_exists_on_drive(file_name: str):
    # return True if file exists
    # else return False
