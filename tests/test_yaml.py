import pytest
from dotcat import run
import sys
from io import StringIO

@pytest.fixture
def yaml_file():
    return "tests/fixtures/test.yaml"

@pytest.fixture
def malformed_yaml_file():
    return "tests/fixtures/malformed.yaml"

@pytest.fixture
def empty_yaml_file():
    return "tests/fixtures/empty.yaml"

def test_yaml_parsing(yaml_file):
    test_args = [yaml_file, 'python.editor.tabSize']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == '4'

def test_yaml_parsing_no_key(yaml_file):
    test_args = [yaml_file, 'python.editor.dictator']
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 5

def test_yaml_key_error(yaml_file):
    test_args = [yaml_file, 'python.editor.unknownKey']
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 5

def test_malformed_yaml(malformed_yaml_file):
    test_args = [malformed_yaml_file, 'python.editor.tabSize']
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 5

def test_empty_yaml(empty_yaml_file):
    test_args = [empty_yaml_file, 'python.editor.tabSize']
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 5
