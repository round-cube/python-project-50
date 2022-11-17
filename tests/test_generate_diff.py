from pytest import mark
from gendiff import generate_diff


MARKS = [
    ("plain/file1.json", "plain/file2.json", "plain/expected_result.txt"),
    ("plain/file1.yaml", "plain/file2.yaml", "plain/expected_result.txt"),
    ("nested/file1.json", "nested/file2.json", "nested/expected_result.txt"),
    ("nested/file1.yaml", "nested/file2.yaml", "nested/expected_result.txt"),
]


@mark.parametrize(
    "file1,file2,diff_result",
    MARKS,
    indirect=["file1", "file2", "diff_result"],
)
def test_generate_diff(file1, file2, diff_result):
    diff = generate_diff(file1, file2)
    assert diff == diff_result
