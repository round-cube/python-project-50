install:
	poetry install

run:
	poetry run gendiff file1.json file2.json

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 .
