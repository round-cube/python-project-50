"""Internal diff representation."""


def _format_value(v):
    """Recursively format value."""
    if type(v) is not dict:
        return v
    properties = []
    for key in v:
        value = v[key]
        formatted_value = _format_value(value)
        property = {"key": key, "value": formatted_value}
        properties.append(property)
    return properties


def _get_new_key_diff_entries(source, compared_to):
    """Process keys that are contained only in self.compared_to"""
    source_keys = set(source.keys())
    compared_keys = set(compared_to.keys())
    for key in compared_keys - source_keys:
        value = compared_to[key]
        yield {"type": "added", "key": key, "value": _format_value(value)}


def _get_commmon_key_diff_entry(source_key, source_value, compared_to):
    """Generate formatted key diff entry."""

    if source_key not in compared_to.keys():
        return {
            "type": "removed",
            "key": source_key,
            "value": _format_value(source_value),
        }

    compared_value = compared_to[source_key]
    types_are_equal = type(source_value) == type(compared_value) == dict
    values_are_different = source_value != compared_value

    if types_are_equal and values_are_different:
        return {
            "key": source_key,
            "value": get_diff_entries(source_value, compared_value),
        }
    elif source_value == compared_value:
        return {"key": source_key, "value": _format_value(source_value)}
    else:
        return {
            "type": "updated",
            "key": source_key,
            "old_value": _format_value(source_value),
            "new_value": _format_value(compared_value),
        }


def get_diff_entries(source, compared_to):
    """Generate diff entries between source and compared_to dicts."""
    diff_entries = []

    for source_key in source:
        source_value = source[source_key]
        entry = _get_commmon_key_diff_entry(
            source_key, source_value, compared_to
        )
        diff_entries.append(entry)

    for diff_entry in _get_new_key_diff_entries(source, compared_to):
        diff_entries.append(diff_entry)
    return diff_entries


def sort_by_key(entries):
    """Recursively sort entries by value."""
    for entry in entries:
        value = entry.get("value")
        if type(value) is list:
            sorted_value = sort_by_key(value)
            entry["value"] = sorted_value
    return sorted(entries, key=lambda x: x["key"])
