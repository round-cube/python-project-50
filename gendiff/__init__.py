from gendiff.files import open_file
from gendiff.diff_entries import DiffEntriesGenerator, sort_by_key
from gendiff.formatters.stylish import format_diff_entries


def generate_diff(file_path1, file_path2, formatter="stylish"):
    source, compared_to = open_file(file_path1), open_file(file_path2)
    diff_entries = DiffEntriesGenerator(source, compared_to).get_entries()
    sorted_diff_entries = sort_by_key(diff_entries)
    return format_diff_entries(sorted_diff_entries)
