# gendiff
[![Actions Status](https://github.com/round-cube/python-project-50/workflows/hexlet-check/badge.svg)](https://github.com/round-cube/python-project-50/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/f67cf2edc025d90f096f/maintainability)](https://codeclimate.com/github/round-cube/python-project-50/maintainability)

Gendiff outputs difference log between two JSON/YAML files. Array values are not supported now.

## Usage
```
usage: gendiff [-h] [-f {stylish,plain,json}] first_file second_file

Compares two configuration files and shows a difference.

positional arguments:
  first_file
  second_file

options:
  -h, --help            show this help message and exit
  -f {stylish,plain,json}, --format {stylish,plain,json}
                        set format of output
```

## Supported output formats

- `json`
- `plain` -- human readable textual log entries
- `stylish` -- default, see example below


## Usage example
[![asciicast](https://asciinema.org/a/qG8CpMcCKucaxFlskSgEMega5.svg)](https://asciinema.org/a/qG8CpMcCKucaxFlskSgEMega5)