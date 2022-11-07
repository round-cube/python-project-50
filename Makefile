install:
	poetry install

run:
	poetry run gendiff tests/files/file1.json tests/files/file2.json

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 .

test:
	poetry run python -m pytest -vvv

