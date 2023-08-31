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
    print("PASS")
