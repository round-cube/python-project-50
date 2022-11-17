DEFAULT_INDENT = 4
DEFAULT_ANNOTATION_POSITION = -2
BAD_ENTRY_TYPE_ERROR = "Bad entry type"
NEW_KEY_ANNOTATION = "+"
REMOVED_KEY_ANNOTATION = "-"


def _get_indent_by_level(level, indent=DEFAULT_INDENT):
    """Get indent by level."""
    return (level + 1) * indent


def _indent_string(
    string_to_indent,
    indent,
    annotation_position=DEFAULT_ANNOTATION_POSITION,
    annotation=None,
):
    """Return string indented by indent number of spaces with annotation
    placed at annotation_position."""
    result = [" " for i in range(indent)]
    if annotation and type(annotation) == str:
        result[annotation_position] = annotation
    result.extend([string_to_indent])
    return "".join(result)


def _format_value(v, level=0):
    """Format value of the property with indent for level."""
    if type(v) is bool:
        return "true" if v else "false"
    elif v is None:
        return "null"
    elif type(v) is list:
        lines = ["{"]
        closing_bracket_level = level
        closing_bracket_indent = _get_indent_by_level(closing_bracket_level)
        prop_level = level + 1
        prop_indent = _get_indent_by_level(prop_level)
        nested_indent = level + 1
        for prop in v:
            key = prop["key"]
            value = prop["value"]
            formatted_value = _format_value(value, level=nested_indent)
            new_line = f"{key}: {formatted_value}"
            indented_line = _indent_string(new_line, prop_indent)
            lines.append(indented_line)
        indented_closing_bracket = _indent_string("}", closing_bracket_indent)
        lines.append(indented_closing_bracket)
        return "\n".join(lines)
    return v


def _process_equal_diff_entry(diff_entry, level):
    key = diff_entry["key"]
    value = _format_value(diff_entry["value"], level=level)
    indent = _get_indent_by_level(level)
    entry_line = _indent_string(f"{key}: {value}", indent)
    entry_lines = [entry_line]
    return entry_lines


def _process_updated_diff_entries(diff_entry, level):
    key = diff_entry["key"]
    old_value = _format_value(diff_entry["old_value"], level=level)
    new_value = _format_value(diff_entry["new_value"], level=level)
    indent = _get_indent_by_level(level)
    old_entry_line = _indent_string(
        f"{key}: {old_value}", indent, annotation=REMOVED_KEY_ANNOTATION
    )
    new_entry_line = _indent_string(
        f"{key}: {new_value}", indent, annotation=NEW_KEY_ANNOTATION
    )
    entry_lines = [old_entry_line, new_entry_line]
    return entry_lines


def _process_removed_diff_entries(diff_entry, level):
    key = diff_entry["key"]
    value = diff_entry["value"]
    formatted_value = _format_value(value, level=level)
    indent = _get_indent_by_level(level)
    entry_line = _indent_string(
        f"{key}: {formatted_value}", indent, annotation=REMOVED_KEY_ANNOTATION
    )
    entry_lines = [entry_line]
    return entry_lines


def _process_added_diff_entries(diff_entry, level):
    key = diff_entry["key"]
    value = diff_entry["value"]
    formatted_value = _format_value(value, level=level)
    indent = _get_indent_by_level(level)
    entry_line = _indent_string(
        f"{key}: {formatted_value}", indent, annotation=NEW_KEY_ANNOTATION
    )
    entry_lines = [entry_line]
    return entry_lines


ENTRY_PROCESSOR = {
    "updated": _process_updated_diff_entries,
    "removed": _process_removed_diff_entries,
    "added": _process_added_diff_entries
}


def format_diff_entries(diff_entries, level=0):
    resulting_lines = ["{"]
    for diff_entry in diff_entries:
        entry_type = diff_entry.get("type")
        entry_lines = []
        if entry_type is not None:
            processor = ENTRY_PROCESSOR[entry_type]
            entry_lines = processor(diff_entry, level)
        else:
            value = diff_entry["value"]
            if type(value) is not list:
                entry_lines = _process_equal_diff_entry(diff_entry, level)
            else:
                key = diff_entry["key"]
                children = value
                nested_level = level + 1
                formatted_value = format_diff_entries(children,
                                                      level=nested_level)
                indent = _get_indent_by_level(level)
                entry_line = _indent_string(f"{key}: {formatted_value}", indent)
                entry_lines = [entry_line]
        resulting_lines.extend(entry_lines)

    indent = _get_indent_by_level(level - 1)
    resulting_lines.append(" " * indent + "}")
    return "\n".join(resulting_lines)
