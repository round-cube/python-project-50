from gendiff.files import open_file
from gendiff.diff_entries import DiffEntriesGenerator, sort_by_key
from gendiff.formatters import stylish
from gendiff.formatters import plain
from gendiff.formatters import json

SUPPORTED_FORMATTERS = ["stylish", "plain", "json"]
SUPPORTED_FORMATTERS_EXC = f"Supported formatters: {SUPPORTED_FORMATTERS}."


def generate_diff(file_path1, file_path2, formatter="stylish"):
    source, compared_to = open_file(file_path1), open_file(file_path2)
    diff_entries = DiffEntriesGenerator(source, compared_to).get_entries()
    sorted_diff_entries = sort_by_key(diff_entries)
    if formatter == "stylish":
        formatter = stylish
    elif formatter == "plain":
        formatter = plain
    elif formatter == "json":
        formatter = json
    else:
        raise ValueError(SUPPORTED_FORMATTERS_EXC)

    return formatter.format_diff_entries(sorted_diff_entries)
