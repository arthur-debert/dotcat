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
    test_args = [toml_file, 'python.editor.tabSize', '--output=raw']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == '4'

def test_output_formatted(toml_file):
    test_args = [toml_file, 'python.editor.tabSize', '--output=formatted']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == '4'

def test_output_json(toml_file):
    test_args = [toml_file, 'python.editor.tabSize', '--output=json']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == '4'

def test_output_yaml(toml_file):
    test_args = [toml_file, 'python.editor.tabSize', '--output=yaml']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == '4'

def test_output_toml(toml_file):
    test_args = [toml_file, 'python.editor.tabSize', '--output=toml']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == '4'

def test_output_ini(toml_file):
    test_args = [toml_file, 'python.editor.tabSize', '--output=ini']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == '4'