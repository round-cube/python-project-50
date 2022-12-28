from pytest import mark
from gendiff import generate_diff


MARKS = [
    (
        "plain/file1.json",
        "plain/file2.json",
        "plain/expected_result.txt",
        "stylish",
    ),
    (
        "plain/file1.yaml",
        "plain/file2.yaml",
        "plain/expected_result.txt",
        "stylish",
    ),
    (
        "nested/file1.json",
        "nested/file2.json",
        "nested/expected_stylish.txt",
        "stylish",
    ),
    (
        "nested/file1.yaml",
        "nested/file2.yaml",
        "nested/expected_stylish.txt",
        "stylish",
    ),
    (
        "nested/file1.json",
        "nested/file2.json",
        "nested/expected_plain.txt",
        "plain",
    ),
    (
        "nested/file1.yaml",
        "nested/file2.yaml",
        "nested/expected_plain.txt",
        "plain",
    ),
    (
        "nested/file1.json",
        "nested/file2.json",
        "nested/expected_json.json",
        "json",
    ),
    (
        "nested/file1.yaml",
        "nested/file2.yaml",
        "nested/expected_json.json",
        "json",
    ),
]


@mark.parametrize(
    "file1,file2,diff_result,format",
    MARKS,
    indirect=["file1", "file2", "diff_result"],
)
def test_generate_diff(file1, file2, diff_result, format):
    diff = generate_diff(file1, file2, format)
    assert diff == diff_result
