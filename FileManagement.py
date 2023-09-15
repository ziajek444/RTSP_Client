import os
import time
from simple_logs import log_info, log_debug, log_error

TO_CONSOLE = True      # Default False


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


def get_last_modification(file_path: str):
    return os.path.getmtime(file_path)


def get_all_files_in_dir(dir: str, expected_ext: str = None):
    print(dir, expected_ext)
    all_files = os.listdir(dir)
    files_to_ret = []
    if isinstance(expected_ext, type(None)):
        files_to_ret = all_files
    else:
        for file in all_files:
            current_ext = extract_extension_from_path(file)
            if current_ext == expected_ext:
                files_to_ret.append(file)
            else:
                print("not match ext: ", current_ext)
    return files_to_ret


# dir = _source_name + "_dir/"
def rm_7z_files_older_than_s(_dir: str, duration_seconds: float):
    all_local_files = get_all_files_in_dir(_dir, expected_ext=".7z")
    all_files_to_rm = []
    for local_file in all_local_files:
        full_path = os.path.join(_dir, local_file)
        not_modified_from_s = get_last_modification(full_path)
        if not_modified_from_s is None:
            continue
        now = time.time()
        diff = now - not_modified_from_s
        if diff > duration_seconds:
            all_files_to_rm.append(full_path)
    log_debug("Files to rm: ", all_files_to_rm, to_console=TO_CONSOLE)

    for file_to_rm in all_files_to_rm:
        try:
            log_debug("Try to remove: ", file_to_rm, "file", to_console=TO_CONSOLE)
            os.remove(file_to_rm)
        except Exception as err:
            log_error("Cannot remove file: ", file_to_rm, to_console=TO_CONSOLE)
        finally:
            pass


def daemon_remove_files_older_than_10min(_dir: str):
    sec = 1.0
    min = sec * 60
    wait_duration = min * 10 * 2
    while True:
        try:
            rm_7z_files_older_than_s(_dir, min*10)
        except Exception as err:
            log_error(f"Exception from rm_files_older_than_s: [{err}]", to_console=TO_CONSOLE)
        finally:
            time.sleep(wait_duration)


if __name__ == "__main__":
    log_info("FileManagement.py testing ", to_console=True)

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

    log_info("PASS", to_console=True)
