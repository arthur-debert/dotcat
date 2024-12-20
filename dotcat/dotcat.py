#! /usr/bin/env python3
"""
This script reads values, including nested values, from structured data files (JSON, YAML, TOML, INI).

Usage:
    dotcat <file> <dot_separated_key>

Example:
    dotcat config.json python.editor.tabSize
    dotcat somefile.toml a.b.c
"""

import sys
import os
import toml
import json
from io import StringIO

def italics(text):
    return f"\033[3m{text}\033[0m"

def bold(text):
    return f"\033[1m{text}\033[0m"

USAGE = f"""
{bold('dotcat')}
Read values, including nested values, from structured data files (JSON, YAML, TOML, INI).

{bold('USAGE:')}
dotcat <file> <dot_separated_key>

{bold('EXAMPLE:')}
dotcat config.json python.editor.tabSize
dotcat somefile.toml a.b.c
"""

def parse_ini(file):
    from configparser import ConfigParser
    config = ConfigParser()
    config.read_file(file)
    return {s: dict(config.items(s)) for s in config.sections()}

FORMATS = [
    ('.json', json.load),
    ('.yaml', lambda f: __import__('yaml').safe_load(f)),
    ('.yml', lambda f: __import__('yaml').safe_load(f)),
    ('.toml', toml.load),
    ('.ini', parse_ini)
]

def todot(adict, lookup_path):
    """
    Accesses a nested dictionary value using a dot-separated string.

    Args:
        adict: The dictionary to access.
        lookup_path: The dot-separated string representing the nested keys.

    Returns:
        The value at the specified nested key, or None if the key doesn't exist.
    """
    found_keys = []
    for key in lookup_path.split('.'):
        adict = adict.get(key)
        if adict is None:
            raise KeyError(f"key '{bold(key)}' not found in {italics('.'.join(found_keys))}")
        found_keys.append(key)
    return adict

def parse_file(filename):
    """
    Tries to parse the file using different formats (JSON, YAML, TOML, INI).

    Args:
        filename: The name of the file to parse.

    Returns:
        The parsed content as a dictionary.
    """
    ext = os.path.splitext(filename)[1].lower()
    parsers = [parser for fmt, parser in FORMATS if fmt == ext]
    parsers += [parser for fmt, parser in FORMATS if fmt != ext]

    for parser in parsers:
        try:
            with open(filename, 'r') as file:
                content = file.read().strip()
                if not content:
                    raise ValueError(f"File is empty: {filename}")
                return parser(StringIO(content))
        except Exception:
            continue
    raise ValueError(f"Unable to parse the file: {filename}")

def run(args):
    """
    Processes the command-line arguments and prints the value from the structured data file.

    Args:
        args: The list of command-line arguments.
    """
    lookup = args.pop()
    filename = args.pop() if args else 'pyproject.toml'
    if not lookup:
        print(USAGE)
        sys.exit(1)
    # load the file
    try:
        data = parse_file(filename)
    except ValueError as e:
        print(e)
        sys.exit(1)
    # get the value at the specified key
    try:
        print(todot(data, lookup))
    except KeyError as e:
        print(f"{filename}: " + e.args[0].strip('"'))
        sys.exit(1)

if __name__ == '__main__':
    run(sys.argv[1:])