import pytest
from dotcat import run
import sys
from io import StringIO

@pytest.fixture
def toml_file():
    return "tests/fixtures/test.toml"



def test_toml_parsing_output_dict(toml_file):
    test_args = [toml_file, 'python.editor.tabSize']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == '4'

def test_output_raw(toml_file):
    test_args = [toml_file, 'python.editor', '--output=raw']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    expected_output = "{'tabSize': 4}\n"
    assert captured_output.getvalue() == expected_output

def test_output_formatted(toml_file):
    test_args = [toml_file, 'python.editor', '--output=formatted']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    expected_output = '{\n    "tabSize": 4\n}\n'
    assert captured_output.getvalue() == expected_output

def test_output_json(toml_file):
    test_args = [toml_file, 'python.editor', '--output=json']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    expected_output = '{\n    "tabSize": 4\n}\n'
    assert captured_output.getvalue() == expected_output

def test_output_yaml(toml_file):
    test_args = [toml_file, 'python.editor', '--output=yaml']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    expected_output = 'tabSize: 4\n\n'
    assert captured_output.getvalue() == expected_output

def test_output_toml(toml_file):
    test_args = [toml_file, 'python.editor', '--output=toml']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    expected_output = 'tabSize = 4\n\n'
    assert captured_output.getvalue() == expected_output

def test_output_ini(toml_file):
    test_args = [toml_file, 'python.editor', '--output=ini']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    expected_output = '[editor]\ntabSize = 4\n'
    assert captured_output.getvalue() == expected_output