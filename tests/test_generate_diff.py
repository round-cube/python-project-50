from pytest import mark
from gendiff import generate_diff


@mark.parametrize(
    "file1,file2,diff_result",
    [("file1.json", "file2.json", "expected_result.txt")],
    indirect=["file1", "file2", "diff_result"])
def test_generate_diff(file1, file2, diff_result):
    assert generate_diff(file1, file2) == diff_result

