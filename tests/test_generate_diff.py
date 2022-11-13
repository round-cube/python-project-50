from pytest import mark
from gendiff import generate_diff


@mark.parametrize(
    "file1,file2,diff_result",
    [("plain/file1.json", "plain/file2.json", "plain/expected_result.txt"),
     ("plain/file1.yaml", "plain/file2.yaml", "plain/expected_result.txt")],
    indirect=["file1", "file2", "diff_result"])
def test_generate_diff(file1, file2, diff_result):
    assert generate_diff(file1, file2) == diff_result

