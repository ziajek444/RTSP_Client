import json

def is_setup_valid(data):
    if not data:
        return False
    if not isinstance(data, dict):
        return False
    if not "parent_directory" in data.keys():
        return False
    if not isinstance(data["parent_directory"], str):
        return False
    if len(data["parent_directory"]) == 0:
        return False

    return True

def setup_data(json_setup_file_path: str = "setup.json"):
    setup_data = None
    with open(json_setup_file_path) as setup_json_file:
        setup_data = json.load(setup_json_file)
    if not is_setup_valid(setup_data):
        print("Invalid setup.json file")
        exit(-1)
