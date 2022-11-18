"""Plain formatter."""

ADDED_PROP_LOG = "Property '{0}' was added with value: {1}"
UPDATED_PROP_LOG = "Property '{0}' was updated. From {1} to {2}"
REMOVED_PROP_LOG = "Property '{0}' was removed"


def _to_str(value):
    value_type = type(value)
    if value_type == list:
        return "[complex value]"
    elif value is None:
        return "null"
    elif value_type is bool:
        return "true" if value else "false"
    elif value_type is str:
        return f"'{value}'"
    return value


def _get_entry_full_key_path(entry, key_path=[]):
    entry_key = entry["key"]
    full_key_path = key_path + [entry_key]
    return full_key_path


def _get_entry_full_key(entry, key_path=[]):
    full_key_path = _get_entry_full_key_path(entry, key_path=key_path)
    key = ".".join(full_key_path)
    return key


def _get_added_log(plain_log, entry, key_path=[]):
    key = _get_entry_full_key(entry, key_path=key_path)
    value = entry["value"]
    log = ADDED_PROP_LOG.format(key, _to_str(value))
    plain_log.append(log)


def _get_removed_log(plain_log, entry, key_path=[]):
    key = _get_entry_full_key(entry, key_path=key_path)
    log = REMOVED_PROP_LOG.format(key)
    plain_log.append(log)


def _get_updated_log(plain_log, entry, key_path=[]):
    key = _get_entry_full_key(entry, key_path=key_path)
    old_value_str = _to_str(entry["old_value"])
    new_value_str = _to_str(entry["new_value"])
    log = UPDATED_PROP_LOG.format(key, old_value_str, new_value_str)
    plain_log.append(log)


ENTRY_TYPE_PROCESSORS = {
    "added": _get_added_log,
    "removed": _get_removed_log,
    "updated": _get_updated_log,
}


def _get_plain_log(sorted_diff_entries, key_path=[]):
    plain_log = []
    for entry in sorted_diff_entries:
        entry_type = entry.get("type")
        process_entry = ENTRY_TYPE_PROCESSORS.get(entry_type)
        if process_entry:
            process_entry(plain_log, entry, key_path=key_path)
        elif entry_type is None and type(entry["value"]) is list:
            nested_types = [e.get("type") for e in entry["value"]]
            if not any(nested_types):
                continue
            full_key_path = _get_entry_full_key_path(entry, key_path=key_path)
            nested_log = _get_plain_log(entry["value"], key_path=full_key_path)
            plain_log.extend(nested_log)
    return plain_log


def format_diff_entries(sorted_diff_entries):
    plain_log = _get_plain_log(sorted_diff_entries)
    return "\n".join(plain_log)
