import json


def sanitize_bool(value):
    if type(value) is bool:
        return "true" if value else "false"
    return value


def generate_diff(file_path1, file_path2):
    with open(file_path1) as f:
        source = json.load(f)

    with open(file_path2) as f:
        compared_to = json.load(f)

    key_text_diffs = []
    for source_key in source:
        source_value = sanitize_bool(source[source_key])
        if source_key in compared_to.keys():
            compared_value = sanitize_bool(compared_to[source_key])
            if source_value == compared_value:
                text_diff = f"    {source_key}: {source_value}"
            else:
                text_diff = f"  - {source_key}: {source_value}\n"\
                            f"  + {source_key}: {compared_value}"
        else:
            text_diff = f"  - {source_key}: {source_value}"

        key_text_diffs.append(text_diff)

    source_keys = set(source.keys())
    compared_keys = set(compared_to.keys())
    for key in compared_keys - source_keys:
        text_diff = f"  + {key}: {compared_to[key]}"
        key_text_diffs.append(text_diff)

    full_text_diff = '\n'.join(key_text_diffs)
    return full_text_diff
