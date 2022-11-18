"""Plain formatter."""

def _to_str(value):
    value_type = type(value)
    if value_type == list:
        return "[complex value]"
    elif value is None:
        return "null"
    elif value_type is bool:
        return 'true' if value else 'false'
    elif value_type is str:
        return f"'{value}'"
    return value


def _get_plain_log(sorted_diff_entries, key_path=[]):
    plain_log = []
    for entry in sorted_diff_entries:
        entry_type = entry.get("type")
        entry_key = entry["key"]
        full_key_path = key_path + [entry_key]
        key = ".".join(full_key_path)
        if entry_type == "added":
            plain_log.append(f"Property '{key}' was added with value: {_to_str(entry['value'])}")
        elif entry_type == "removed":
            plain_log.append(f"Property '{key}' was removed")
        elif entry_type == "updated":
            old_value_str = _to_str(entry['old_value'])
            new_value_str = _to_str(entry['new_value'])
            plain_log.append(f"Property '{key}' was updated. From {old_value_str} to {new_value_str}")
        elif entry_type is None and type(entry["value"]) is list:
            nested_types = [e.get("type") for e in entry["value"]]
            if not any(nested_types):
                continue
            nested_log = _get_plain_log(entry["value"], key_path=full_key_path)
            plain_log.extend(nested_log)
    return plain_log


def format_diff_entries(sorted_diff_entries):
    plain_log = _get_plain_log(sorted_diff_entries)
    return "\n".join(plain_log)