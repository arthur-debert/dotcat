import pytest
from dotcat import run
import sys
from io import StringIO

@pytest.fixture
def json_file(tmp_path):
    file_path = tmp_path / "test.json"
    file_path.write_text('{"python": {"editor": {"tabSize": 4}}}')
    return file_path

@pytest.fixture
def malformed_json_file(tmp_path):
    file_path = tmp_path / "malformed.json"
    file_path.write_text('{"python": {"editor": {"tabSize": 4}')
    return file_path

@pytest.fixture
def empty_json_file(tmp_path):
    file_path = tmp_path / "empty.json"
    file_path.write_text('{}')
    return file_path

def test_json_parsing(monkeypatch, json_file):
    test_args = ['dotcat', str(json_file), 'python.editor.tabSize']
    monkeypatch.setattr('sys.argv', test_args)
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args[1:])
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == '4'

def test_json_parsing_no_key(monkeypatch, json_file):
    test_args = ['dotcat', str(json_file), 'python.editor.dictator']
    monkeypatch.setattr('sys.argv', test_args)
    captured_output = StringIO()
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args[1:])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

def test_json_key_error(monkeypatch, json_file):
    test_args = ['dotcat', str(json_file), 'python.editor.unknownKey']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args[1:])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

def test_malformed_json(monkeypatch, malformed_json_file):
    test_args = ['dotcat', str(malformed_json_file), 'python.editor.tabSize']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args[1:])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

def test_empty_json(monkeypatch, empty_json_file):
    test_args = ['dotcat', str(empty_json_file), 'python.editor.tabSize']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args[1:])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
