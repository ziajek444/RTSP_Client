import os


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
    return os.path.basename(path_to_file)


def extract_base_path_from_path(path_to_file: str):
    return os.path.dirname(path_to_file)


def extract_extension_from_path(path_to_file: str):
    return os.path.splitext(path_to_file)[1]


def extract_path_without_extension(path_to_file: str):
    return os.path.splitext(path_to_file)[0]


# TODO
def get_all_files_in_dir(dir: str, expected_ext: str = None):
    if isinstance(expected_ext, type(None)):
        # => all files in passed dir
        return None
    else:
        # => all files in passed dir with specified extension
        return None
    pass


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
