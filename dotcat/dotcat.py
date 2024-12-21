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
from io import StringIO
from typing import Any, Dict

def italics(text: str) -> str:
    """
    Returns the given text formatted in italics.

    Args:
        text: The text to format.

    Returns:
        The formatted text.
    """
    return f"\033[3m{text}\033[0m"

def bold(text: str) -> str:
    """
    Returns the given text formatted in bold.

    Args:
        text: The text to format.

    Returns:
        The formatted text.
    """
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

def parse_ini(file: StringIO) -> Dict[str, Dict[str, str]]:
    """
    Parses an INI file and returns its content as a dictionary.

    Args:
        file: The file object to parse.

    Returns:
        The parsed content as a dictionary.
    """
    from configparser import ConfigParser
    config = ConfigParser()
    config.read_file(file)
    return {s: dict(config.items(s)) for s in config.sections()}

def parse_yaml(file: StringIO) -> Any:
    """
    Parses a YAML file and returns its content.

    Args:
        file: The file object to parse.

    Returns:
        The parsed content.
    """
    import yaml
    return yaml.safe_load(file)

def parse_json(file: StringIO) -> Any:
    """
    Parses a JSON file and returns its content.

    Args:
        file: The file object to parse.

    Returns:
        The parsed content.
    """
    import json
    return json.load(file)

def parse_toml(file: StringIO) -> Any:
    """
    Parses a TOML file and returns its content.

    Args:
        file: The file object to parse.

    Returns:
        The parsed content.
    """
    import toml
    return toml.load(file)

FORMATS = [
    (['.json'], parse_json),
    (['.yaml', '.yml'], parse_yaml),
    (['.toml'], parse_toml),
    (['.ini'], parse_ini)
]

def todot(adict: dict, lookup_path: str) -> Any:
    """
    Accesses a nested dictionary value using a dot-separated string.

    Args:
        adict: The dictionary to access.
        lookup_path: The dot-separated string representing the nested keys.

    Returns:
        The value at the specified nested key, or None if the key doesn't exist.
    """
    if adict is None:
        raise KeyError(f"key '{bold(lookup_path.split('.')[0])}' not found in {italics('')}")
    found_keys = []
    for key in lookup_path.split('.'):
        adict = adict.get(key)
        if adict is None:
            raise KeyError(f"key '{key}' not found in {'.'.join(found_keys)}")
        found_keys.append(key)
    return adict

def parse_file(filename: str) -> Dict[str, Any]:
    """
    Tries to parse the file using different formats (JSON, YAML, TOML, INI).

    Args:
        filename: The name of the file to parse.

    Returns:
        The parsed content as a dictionary.
    """
    ext = os.path.splitext(filename)[1].lower()
    parsers = [parser for fmts, parser in FORMATS if ext in fmts]

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

def run(args: list[str] = None) -> None:
    """
    Processes the command-line arguments and prints the value from the structured data file.

    Args:
        args: The list of command-line arguments.
    """
    if args is None:
        print(USAGE)
    elif len(args) != 2:
        print(USAGE)
        sys.exit(1)

    filename, lookup = args
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

def main() -> None:
    """
    The main entry point of the script.
    """
    run(sys.argv[1:])

if __name__ == '__main__':
    main()