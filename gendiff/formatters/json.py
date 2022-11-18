from json import dumps


def format_diff_entries(diff_entries):
    return dumps(diff_entries, indent=4)
