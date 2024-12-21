#! /usr/bin/env python3
"""
This script reads values, including nested values, from structured data files (JSON, YAML, TOML, INI).

Usage:
    dotcat <file> <dot_separated_key>

Example:
    dotcat config.json python.editor.tabSize
    dotcat somefile.toml a.b.c

Exit Codes:
    2: Invalid usage (wrong number of arguments)
    3: File not found
    4: Parsing error
    5: Key not found
"""

import sys
import os
from io import StringIO
from typing import Any, Dict, List, Union

ParsedData = Union[Dict[str, Any], List[Any]]

class ParseError(Exception):
    """Custom exception for parsing errors."""
    pass

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

def parse_yaml(file: StringIO) -> ParsedData:
    """
    Parses a YAML file and returns its content.

    Args:
        file: The file object to parse.

    Returns:
        The parsed content.
    """
    import yaml
    try:
        return yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise ParseError(f"[ERROR] {file.name}: Unable to parse YAML file: {str(e)}")

def parse_json(file: StringIO) -> ParsedData:
    """
    Parses a JSON file and returns its content.

    Args:
        file: The file object to parse.

    Returns:
        The parsed content.
    """
    import json
    try:
        return json.load(file)
    except json.JSONDecodeError as e:
        raise ParseError(f"[ERROR] {file.name}: Unable to parse JSON file: {str(e)}")

def parse_toml(file: StringIO) -> ParsedData:
    """
    Parses a TOML file and returns its content.

    Args:
        file: The file object to parse.

    Returns:
        The parsed content.
    """
    import toml
    try:
        return toml.load(file)
    except toml.TomlDecodeError as e:
        raise ParseError(f"[ERROR] {file.name}: Unable to parse TOML file: {str(e)}")

FORMATS = [
    (['.json'], parse_json),
    (['.yaml', '.yml'], parse_yaml),
    (['.toml'], parse_toml),
    (['.ini'], parse_ini)
]

def from_attr_chain(data: Dict[str, Any], lookup_chain: str) -> Any:
    """
    Accesses a nested dictionary value with an attribute chain encoded by a dot-separated string.

    Args:
        adict: The dictionary to access.
        lookup_path: The dot-separated string representing the nested keys.

    Returns:
        The value at the specified nested key, or None if the key doesn't exist.
    """
    if data is None:
        raise KeyError(f"[ERROR] key '{bold(lookup_chain.split('.')[0])}' not found in {italics('')}")
    found_keys = []
    for key in lookup_chain.split('.'):
        data = data.get(key)
        if data is None:
            raise KeyError(f"[ERROR] key '{key}' not found in {'.'.join(found_keys)}")
        found_keys.append(key)
    return data

def parse_file(filename: str) -> ParsedData:
    """
    Tries to parse the file using different formats (JSON, YAML, TOML, INI).

    Args:
        filename: The name of the file to parse.

    Returns:
        The parsed content as a dictionary or list.
    """
    ext = os.path.splitext(filename)[1].lower()
    parsers = [parser for fmts, parser in FORMATS if ext in fmts]

    try:
        with open(filename, 'r') as file:
            content = file.read().strip()
            if not content:
                raise ValueError(f"[ERROR] {filename}: File is empty")
            for parser in parsers:
                try:
                    return parser(StringIO(content))
                except ParseError:
                    continue
            raise ValueError(f"[ERROR] {filename}: Unsupported file format. Supported formats: JSON, YAML, TOML, INI")
    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR] {filename}: File not found")
    except Exception as e:
        raise ValueError(f"[ERROR] {filename}: Unable to parse file: {str(e)}")

def run(args: List[str] = None) -> None:
    """
    Processes the command-line arguments and prints the value from the structured data file.

    Args:
        args: The list of command-line arguments.
    """
    # validates arguments
    if args is None:
        print(USAGE)
    elif len(args) != 2:
        print(USAGE)
        sys.exit(2)  # Invalid usage
    filename, lookup_chain = args

    # gets the parsed data
    try:
        data = parse_file(filename)
    except FileNotFoundError as e:
        print(e)
        sys.exit(3)  # File not found
    except ValueError as e:
        print(e)
        sys.exit(4)  # Parsing error

    # get the value at the specified key
    try:
        print(from_attr_chain(data, lookup_chain))
    except KeyError as e:
        print(f"[ERROR] {filename}: " + e.args[0].strip('"'))
        sys.exit(5)  # Key not found

def main() -> None:
    """
    The main entry point of the script.
    """
    run(sys.argv[1:])

if __name__ == '__main__':
    main()