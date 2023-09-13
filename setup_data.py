import json
from simple_logs import log_critical


__SETUP_KEYWORDS = dict({"parent_directory": str, "test_key": int})


def is_setup_valid(data: dict):
    if not data or not isinstance(data, dict):
        log_critical("is_setup_valid: setup file has invalid structure")
        return False
    are_true = list(map(lambda d_obj: d_obj[0] in data.keys(), __SETUP_KEYWORDS.items()))
    if not all(are_true):
        log_critical("is_setup_valid: missing required keywords in setup file")
        return False
    are_true = list(map(lambda d_obj: isinstance(data[d_obj[0]], d_obj[1]), __SETUP_KEYWORDS.items()))
    if not all(are_true):
        log_critical("is_setup_valid: values of keywords in setup file have wrong type")
        return False

    return are_values_correct(data)


def are_values_correct(data: dict):
    google_drive_director_id_len = 33
    if len(data["parent_directory"]) != google_drive_director_id_len:
        log_critical("are_values_correct: parent_directory google drive id length (33) is invalid")
        return False
    return True


def setup_json_data(json_setup_file_path: str = "setup.json"):
    setup_data = None
    with open(json_setup_file_path) as setup_json_file:
        setup_data = json.load(setup_json_file)
    if not is_setup_valid(setup_data):
        log_critical("setup_json_data: exit app", to_console=True)
        exit(-1)
    return setup_data
