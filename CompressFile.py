import py7zr
import os
from FileManagement import dir_exists, extract_file_name_from_path, extract_base_path_from_path


def compress_files(path_to_file_list: list, arch_path_to_file: str):
    _filters = [{'id': py7zr.FILTER_PPMD, 'order': 6, 'mem': "256m", 'level': 9}]
    existing_files = list()
    for path_to_file in path_to_file_list:
        if dir_exists(path_to_file):
            existing_files.append(path_to_file)

    with py7zr.SevenZipFile(arch_path_to_file, 'w', filters=_filters) as archive:
        for existing_file in existing_files:
            archive.write(existing_file, extract_file_name_from_path(existing_file))


def decompress_archive(path_to_archive: str):
    with py7zr.SevenZipFile(path_to_archive, 'r') as archive:
        archive.extract(extract_base_path_from_path(path_to_archive))


if __name__ == "__main__":
    print("testing Compress file py7zr")
    pwd = os.getcwd() + "\\"
    test_dir = pwd + "test_dir\\"
    archive_name = "Archive.7z"
    arch_path_to_file = test_dir + archive_name
    test_clip_name = "test_clip.mp4"
    test_clip_path_to_file = test_dir + test_clip_name

    assert dir_exists(arch_path_to_file) is True
    assert dir_exists(test_clip_path_to_file) is False
    decompress_archive(arch_path_to_file)
    assert dir_exists(arch_path_to_file) is True
    assert dir_exists(test_clip_path_to_file) is True
    os.remove(arch_path_to_file)
    assert dir_exists(arch_path_to_file) is False
    assert dir_exists(test_clip_path_to_file) is True
    compress_files([test_clip_path_to_file], arch_path_to_file)
    assert dir_exists(arch_path_to_file) is True
    assert dir_exists(test_clip_path_to_file) is True
    os.remove(test_clip_path_to_file)
    assert dir_exists(arch_path_to_file) is True
    assert dir_exists(test_clip_path_to_file) is False

    print("done")
