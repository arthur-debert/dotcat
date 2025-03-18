import pytest
from dotcat.cli import run
import sys
from io import StringIO


@pytest.fixture
def json_file():
    return "tests/fixtures/test.json"


@pytest.fixture
def malformed_json_file():
    return "tests/fixtures/malformed.json"


@pytest.fixture
def empty_json_file():
    return "tests/fixtures/empty.json"


def test_json_parsing(json_file):
    test_args = [json_file, "python.editor.tabSize"]
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == "4"


def test_json_parsing_no_key(json_file):
    test_args = [json_file, "python.editor.dictator"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 5


def test_json_key_error(json_file):
    test_args = [json_file, "python.editor.unknownKey"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 5


def test_malformed_json(malformed_json_file):
    test_args = [malformed_json_file, "python.editor.tabSize"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 4


def test_empty_json(empty_json_file):
    test_args = [empty_json_file, "python.editor.tabSize"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 5
