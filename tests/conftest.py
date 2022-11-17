from pytest import fixture


@fixture
def file1(request):
    yield f"tests/files/{request.param}"


@fixture
def file2(request):
    yield f"tests/files/{request.param}"


@fixture
def diff_result(request):
    file_path = request.param
    with open(f"tests/files/{file_path}") as f:
        yield f.read()
