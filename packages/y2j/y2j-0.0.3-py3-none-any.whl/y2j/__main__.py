#!/usr/bin/env python
import argparse
import json
import sys

import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', default=None,
                        help='File to translate. Defaults to stdin.')
    parser.add_argument('-c', '--compressed', action='store_true',
                        help='Print JSON with no superfluous whitespace.')
    parser.add_argument('-p', '--pretty', action='store_true',
                        help='Enables pretty-printing of JSON')
    args = parser.parse_args()

    indent = 2 if args.pretty else None
    separators = (',', ':') if not args.pretty and args.compressed else None

    if args.file is not None:
        with open(args.file, 'r') as stream:
            data = yaml.safe_load(stream)
    else:
        if sys.stdin.isatty():
            sys.stderr.write('Warning: reading interactively from stdin.\n')
        data = yaml.safe_load(sys.stdin)

    sys.stdout.write(json.dumps(data, indent=indent, separators=separators))

if __name__ == '__main__':
    main()
