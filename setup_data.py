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
