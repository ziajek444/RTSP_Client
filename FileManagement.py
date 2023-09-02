import os

##7z a -t7z -m0=lzma -mx=9 -mfb=64 -md=32m -ms=on archive.7z dir1
##adds all files from directory "dir1" to archive archive.7z using "ultra settings"

def create_dir(_newDir: str):
    parenDir = os.getcwd()
    path = os.path.join(parenDir, _newDir)
    if os.path.exists(path):
        return -1
    else:
        os.mkdir(path)
        if not os.path.exists(path):
            return -2
        else:
            return 0


def remove_dir(_newDir: str):
    parenDir = os.getcwd()
    path = os.path.join(parenDir, _newDir)
    if not os.path.exists(path):
        return -1
    else:
        os.removedirs(path)
        if os.path.exists(path):
            return -2
        return 0


def dir_exists(dir: str):
    parenDir = os.getcwd()
    path = os.path.join(parenDir, dir)
    if os.path.exists(path):
        return True
    return False


def extract_file_name_from_path(path_to_file: str):
    extension_exists = path_to_file.find('.') > 1
    path_to_file = path_to_file.replace('/', '.')
    path_to_file = path_to_file.replace('\\', '.')
    splited_path = path_to_file.split('.')
    if extension_exists:
        return '.'.join(splited_path[-2:])
    else:
        return splited_path[-1]


def extract_base_path_from_path(path_to_file: str):
    return os.path.dirname(path_to_file)


if __name__ == "__main__":
    print("FileManagement.py testing ")

    assert dir_exists("dumm") is False
    assert 0 == create_dir("dumm")
    assert dir_exists("dumm") is True
    assert -1 == create_dir("dumm")
    assert dir_exists("dumm") is True
    assert 0 == remove_dir("dumm")
    assert dir_exists("dumm") is False
    assert -1 == remove_dir("dumm")
    assert dir_exists("dumm") is False

    assert extract_file_name_from_path(
        r"C:\Users\user_name\Desktop\Directory\sub_directory\file_name.ext") == "file_name.ext"
    assert extract_file_name_from_path(
        r"C:\Users\user_name\Desktop\Directory\sub_directory\file_name") == "file_name"
    assert extract_file_name_from_path(
        "C:\\Users\\user_name\\Desktop\\Directory\\sub_directory\\file_name.ext") == "file_name.ext"
    assert extract_file_name_from_path(
        "C:\\Users\\user_name\\Desktop\\Directory\\sub_directory\\file_name") == "file_name"
    assert extract_file_name_from_path(
        r"C:\\Users\\user_name\\Desktop\\Directory\\sub_directory\\file_name.ext") == "file_name.ext"
    assert extract_file_name_from_path(
        r"C:\\Users\\user_name\\Desktop\\Directory\\sub_directory\\file_name") == "file_name"
    assert extract_file_name_from_path(
        r"C:/Users/user_name/Desktop/Directory/sub_directory/file_name.ext") == "file_name.ext"
    assert extract_file_name_from_path(
        r"C:/Users/user_name/Desktop/Directory/sub_directory/file_name") == "file_name"
    assert extract_file_name_from_path(
        r"C://Users//user_name//Desktop//Directory//sub_directory//file_name.ext") == "file_name.ext"
    assert extract_file_name_from_path(
        r"C://Users//user_name//Desktop//Directory//sub_directory//file_name") == "file_name"

    assert extract_base_path_from_path(
        r"C://Users//user_name//Desktop//Directory//sub_directory//file_name.ext") == r"C://Users//user_name//Desktop//Directory//sub_directory"
    assert extract_base_path_from_path(
        r"C:/Users/user_name/Desktop/Directory/sub_directory/file_name.ext") == r"C:/Users/user_name/Desktop/Directory/sub_directory"
    assert extract_base_path_from_path(
        r"C:\\Users\\user_name\\Desktop\\Directory\\sub_directory\\file_name.ext") == r"C:\\Users\\user_name\\Desktop\\Directory\\sub_directory"
    assert extract_base_path_from_path(
        r"C:\Users\user_name\Desktop\Directory\sub_directory\file_name.ext") == r"C:\Users\user_name\Desktop\Directory\sub_directory"
    assert extract_base_path_from_path(
        "C:\\Users\\user_name\\Desktop\\Directory\\sub_directory\\file_name.ext") == "C:\\Users\\user_name\\Desktop\\Directory\\sub_directory"
    assert extract_base_path_from_path(
        r"C://Users//user_name//Desktop//Directory//sub_directory//file_name") == r"C://Users//user_name//Desktop//Directory//sub_directory"
    assert extract_base_path_from_path(
        r"C:/Users/user_name/Desktop/Directory/sub_directory/file_name") == r"C:/Users/user_name/Desktop/Directory/sub_directory"
    assert extract_base_path_from_path(
        r"C:\\Users\\user_name\\Desktop\\Directory\\sub_directory\\file_name") == r"C:\\Users\\user_name\\Desktop\\Directory\\sub_directory"
    assert extract_base_path_from_path(
        r"C:\Users\user_name\Desktop\Directory\sub_directory\file_name") == r"C:\Users\user_name\Desktop\Directory\sub_directory"
    assert extract_base_path_from_path(
        "C:\\Users\\user_name\\Desktop\\Directory\\sub_directory\\file_name") == "C:\\Users\\user_name\\Desktop\\Directory\\sub_directory"

    print("PASS")
