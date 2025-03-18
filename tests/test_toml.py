import pytest
from dotcat.cli import run
import sys
from io import StringIO


@pytest.fixture
def toml_file():
    return "tests/fixtures/test.toml"


@pytest.fixture
def malformed_toml_file():
    return "tests/fixtures/malformed.toml"


@pytest.fixture
def empty_toml_file():
    return "tests/fixtures/empty.toml"


def test_toml_parsing(toml_file):
    test_args = [toml_file, "python.editor.tabSize"]
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == "4"


def test_toml_parsing_no_key(toml_file):
    test_args = [toml_file, "python.editor.dictator"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 5


def test_toml_key_error(toml_file):
    test_args = [toml_file, "python.editor.unknownKey"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 5


def test_malformed_toml(malformed_toml_file):
    test_args = [malformed_toml_file, "python.editor.tabSize"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 4


def test_empty_toml(empty_toml_file):
    test_args = [empty_toml_file, "python.editor.tabSize"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 5
