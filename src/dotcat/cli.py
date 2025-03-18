"""
Command-line interface functions for dotcat.
"""

import sys
import os
import argparse
from typing import List, Tuple

from .__version__ import __version__
from .formatting import red
from .help_text import HELP, USAGE
from .parsers import parse_file
from .output_formatters import format_output
from .data_access import from_attr_chain


def parse_args(args: List[str]) -> Tuple[str, str, str, bool]:
    """
    Returns the filename, dotted-path, output format, and version flag.

    Args:
        args: The list of command-line arguments.

    Returns:
        The filename, dotted-path, output format, and version flag.
    """
    # Handle help commands
    if args is None or len(args) == 0:
        print(HELP)  # Show help for no arguments
        sys.exit(0)

    # Handle explicit help requests
    if "help" in args or "-h" in args or "--help" in args:
        print(HELP)  # Show help for help requests
        sys.exit(0)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("file", type=str, nargs="?", help="The file to read from")
    parser.add_argument(
        "dotted_path",
        type=str,
        nargs="?",
        help="The dotted-path to look up",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="raw",
        help="The output format (raw, formatted, json, yaml, toml, ini)",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information",
    )

    parsed_args = parser.parse_args(args)
    return (
        parsed_args.file,
        parsed_args.dotted_path,
        parsed_args.output,
        parsed_args.version,
    )


def is_likely_dot_path(arg: str) -> bool:
    """
    Determines if an argument is likely a dotted-path rather than a file path.

    Args:
        arg: The argument to check.

    Returns:
        True if the argument is likely a dot path, False otherwise.
    """
    # If it contains dots and doesn't look like a file path
    if "." in arg and not os.path.exists(arg):
        # Check if it has multiple segments separated by dots
        return len(arg.split(".")) > 1
    return False


def run(args: List[str] = None) -> None:
    """
    Processes the command-line arguments and prints the value from the structured data file.

    Args:
        args: The list of command-line arguments.
    """
    # validates arguments
    filename, lookup_chain, output_format, version_flag = parse_args(args)

    if version_flag:
        print(f"dotcat version {__version__}")
        return

    # Special case: If we have only one argument and it looks like a dotted-path,
    # treat it as the dotted-path rather than the file
    if filename is not None and lookup_chain is None and len(args) == 1:
        if is_likely_dot_path(filename):
            # Swap the arguments
            lookup_chain = filename
            filename = None
            # Now filename is None and lookup_chain is not None

    # Handle cases where one of the required arguments is missing
    if lookup_chain is None or filename is None:
        if filename is not None and lookup_chain is None:
            # Case 1: File is provided but dotted-path is missing
            try:
                if os.path.exists(filename):
                    # File exists, but dotted-path is missing
                    print(
                        f"Dotted-path required. Which value do you want me to look up in {filename}?"
                    )
                    print(f"\n$dotcat {filename} {red('<dotted-path>')}")
                    sys.exit(2)  # Invalid usage
            except Exception:
                # If there's any error checking the file, fall back to general usage message
                pass
        elif filename is None and lookup_chain is not None:
            # Case 2: Dotted-path is provided but file is missing
            # Check if the argument looks like a dotted-path (contains dots)
            if "." in lookup_chain:
                # It looks like a dotted-path, so assume the file is missing
                print(
                    f"File path required. Which file contains the value at {lookup_chain}?"
                )
                print(f"\n$dotcat {red('<file>')} {lookup_chain}")
                sys.exit(2)  # Invalid usage
            # Otherwise, it might be a file without an extension or something else,
            # so fall back to the general usage message

        # General usage message for other cases
        print(USAGE)  # Display usage for invalid arguments
        sys.exit(2)  # Invalid usage

    # gets the parsed data
    try:
        data = parse_file(filename)
    except FileNotFoundError as e:
        print(str(e))
        sys.exit(3)  # File not found
    except ValueError as e:
        if "File is empty" in str(e):
            print(f"{red('[ERROR]')} {filename}: File is empty")
        elif "Unable to parse file" in str(e):
            print(f"Unable to parse file: {red(filename)}")
        else:
            print(f"{str(e)}: {red(filename)}")
        sys.exit(4)  # Parsing error

    # get the value at the specified key
    try:
        value = from_attr_chain(data, lookup_chain)
        print(format_output(value, output_format))
    except KeyError as e:
        key = e.args[0].split("'")[1] if "'" in e.args[0] else e.args[0]
        print(f"Key {red(key)} not found in {filename}")
        sys.exit(5)  # Key not found


def main() -> None:
    """
    The main entry point of the script.
    """
    run(sys.argv[1:])
