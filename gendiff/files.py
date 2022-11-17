from pathlib import Path
from json import load as load_json
from yaml import load as load_yaml, Loader


class BadExtension(Exception):
    pass


YAML_EXTENSIONS = (".yaml", ".yml")
JSON_EXTENSIONS = (".json",)
SUPPORTED_EXTENSIONS = YAML_EXTENSIONS + JSON_EXTENSIONS

BAD_EXCEPTION_TEXT = (
    "File {0} has unaccepted extension type. "
    f"Supported extension types are: [{','.join(SUPPORTED_EXTENSIONS)}]."
)


def open_file(path):
    """Open a file and return Python representation."""
    path = Path(path)
    extension = path.suffix
    with open(path) as f:
        if extension in YAML_EXTENSIONS:
            return load_yaml(f, Loader=Loader)
        elif extension in JSON_EXTENSIONS:
            return load_json(f)
        else:
            raise BadExtension(BAD_EXCEPTION_TEXT.format(path))
