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


def test_argument_parsing_default_output():
    test_args = ['tests/fixtures/complex.yaml', 'name']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = captured_output.getvalue().strip()
    assert actual_output == 'Example'

def test_argument_parsing_raw_output():
    test_args = ['tests/fixtures/complex.yaml', 'name', '--output', 'raw']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = captured_output.getvalue().strip()
    assert actual_output == 'Example'

def test_argument_parsing_formatted_output():
    test_args = ['tests/fixtures/complex.yaml', 'address', '--output', 'formatted']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = captured_output.getvalue().strip()
    assert actual_output.startswith('{') and actual_output.endswith('}')

def test_argument_parsing_json_output():
    test_args = ['tests/fixtures/complex.yaml', 'phones', '--output', 'json']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = captured_output.getvalue().strip()
    assert actual_output.startswith('[') and actual_output.endswith(']')

def test_argument_parsing_yaml_output():
    test_args = ['tests/fixtures/complex.yaml', 'emails', '--output', 'yaml']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = captured_output.getvalue().strip()
    assert actual_output.startswith('-') and 'personal' in actual_output

def test_argument_parsing_toml_output():
    test_args = ['tests/fixtures/complex.yaml', 'projects', '--output', 'toml']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = captured_output.getvalue().strip()
    assert actual_output.startswith('[[items]]') # Updated assertion


def test_argument_parsing_ini_output():
    test_args = ['tests/fixtures/complex.yaml', 'address', '--output', 'ini']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = captured_output.getvalue().strip()
    assert actual_output.startswith('[default]')
