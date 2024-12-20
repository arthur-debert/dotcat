import pytest
from dotcat import run
import sys
from io import StringIO

@pytest.fixture
def yaml_file(tmp_path):
    file_path = tmp_path / "test.yaml"
    file_path.write_text('python:\n  editor:\n    tabSize: 4')
    return file_path

@pytest.fixture
def malformed_yaml_file(tmp_path):
    file_path = tmp_path / "malformed.yaml"
    file_path.write_text('python:\n  editor:\n    tabSize: 4\n  editor:')
    return file_path

@pytest.fixture
def empty_yaml_file(tmp_path):
    file_path = tmp_path / "empty.yaml"
    file_path.write_text('')
    return file_path

def test_yaml_parsing(yaml_file):
    test_args = [str(yaml_file), 'python.editor.tabSize']
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == '4'

def test_yaml_parsing_no_key(yaml_file):
    test_args = [str(yaml_file), 'python.editor.dictator']
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

def test_yaml_key_error(yaml_file):
    test_args = [str(yaml_file), 'python.editor.unknownKey']
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

def test_malformed_yaml(malformed_yaml_file):
    test_args = [str(malformed_yaml_file), 'python.editor.tabSize']
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

def test_empty_yaml(empty_yaml_file):
    test_args = [str(empty_yaml_file), 'python.editor.tabSize']
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
