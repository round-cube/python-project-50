from argparse import ArgumentParser


NAME = "gendiff"
DESCRIPTION = "Compares two configuration files and shows a difference."


def build_parser():
    parser = ArgumentParser(
        prog=NAME,
        description=DESCRIPTION)

    parser.add_argument("first_file")
    parser.add_argument("second_file")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    first_file, second_file = args.first_file, args.second_file
    print(f"succesfully read {first_file} {second_file}")
