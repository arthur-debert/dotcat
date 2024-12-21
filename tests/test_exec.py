from io import StringIO
import sys
from dotcat import run

import pytest


def remove_ansi_escape_sequences(text):
    import re
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)


def test_no_arguments():
    test_args = []
    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    sys.stdout = sys.__stdout__
    expected_output = """
dotcat
Read values, including nested values, from structured data files (JSON, YAML, TOML, INI).

USAGE:
dotcat <file> <dot_separated_key>

EXAMPLE:
dotcat config.json python.editor.tabSize
dotcat somefile.toml a.b.c
""".strip()
    actual_output = remove_ansi_escape_sequences(captured_output.getvalue().strip())
    assert actual_output == expected_output
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2