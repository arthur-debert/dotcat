from io import StringIO
import sys
from dotcat import run, HELP

import pytest


def remove_ansi_escape_sequences(text):
    import re

    ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", text)


def test_no_arguments():
    test_args = []
    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    sys.stdout = sys.__stdout__
    expected_output = remove_ansi_escape_sequences(HELP.strip())
    actual_output = remove_ansi_escape_sequences(captured_output.getvalue().strip())
    assert actual_output == expected_output
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0  # Changed from 2 to 0 to match new behavior


def test_argument_parsing_default_output():
    test_args = ["tests/fixtures/complex.yaml", "name"]
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = captured_output.getvalue().strip()
    assert actual_output == "Example"


def test_argument_parsing_raw_output():
    test_args = ["tests/fixtures/complex.yaml", "name", "--output", "raw"]
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = captured_output.getvalue().strip()
    assert actual_output == "Example"


def test_argument_parsing_formatted_output():
    test_args = ["tests/fixtures/complex.yaml", "address", "--output", "formatted"]
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = captured_output.getvalue().strip()
    assert actual_output.startswith("{") and actual_output.endswith("}")


def test_argument_parsing_json_output():
    test_args = ["tests/fixtures/complex.yaml", "phones", "--output", "json"]
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = captured_output.getvalue().strip()
    assert actual_output.startswith("[") and actual_output.endswith("]")


def test_argument_parsing_yaml_output():
    test_args = ["tests/fixtures/complex.yaml", "emails", "--output", "yaml"]
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = captured_output.getvalue().strip()
    assert actual_output.startswith("-") and "personal" in actual_output


def test_argument_parsing_toml_output():
    test_args = ["tests/fixtures/complex.yaml", "projects", "--output", "toml"]
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = captured_output.getvalue().strip()
    assert actual_output.startswith("[[items]]")  # Updated assertion


def test_argument_parsing_ini_output():
    test_args = ["tests/fixtures/complex.yaml", "address", "--output", "ini"]
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = captured_output.getvalue().strip()
    assert actual_output.startswith("[default]")


def test_check_install():
    test_args = ["--check-install"]
    captured_output = StringIO()
    sys.stdout = captured_output
    run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = captured_output.getvalue().strip()
    assert actual_output == "Dotcat is good to go."


def test_file_without_dot_pattern():
    test_args = ["tests/fixtures/test.json"]
    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = remove_ansi_escape_sequences(captured_output.getvalue().strip())
    # Check that the output contains the specific file name and guidance
    assert "Dotted-path required" in actual_output
    assert "tests/fixtures/test.json" in actual_output
    assert "<dotted-path>" in actual_output
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


def test_dot_path_without_file():
    test_args = ["python.editor.tabSize"]
    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    sys.stdout = sys.__stdout__
    actual_output = remove_ansi_escape_sequences(captured_output.getvalue().strip())
    # Check that the output contains the specific dot path and guidance
    assert "File path required" in actual_output
    assert "python.editor.tabSize" in actual_output
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


def test_help_command():
    test_args = ["help"]
    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    sys.stdout = sys.__stdout__
    expected_output = remove_ansi_escape_sequences(HELP.strip())
    actual_output = remove_ansi_escape_sequences(captured_output.getvalue().strip())
    assert actual_output == expected_output
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0  # Should exit with code 0 for help


def test_help_flag():
    test_args = ["--help"]
    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run(test_args)
    sys.stdout = sys.__stdout__
    expected_output = remove_ansi_escape_sequences(HELP.strip())
    actual_output = remove_ansi_escape_sequences(captured_output.getvalue().strip())
    assert actual_output == expected_output
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0  # Should exit with code 0 for help


def test_help_outputs_match():
    """Test that all three help command forms produce the same output."""
    # Capture output for no arguments
    no_args_output = StringIO()
    sys.stdout = no_args_output
    with pytest.raises(SystemExit):
        run([])
    sys.stdout = sys.__stdout__
    no_args_text = remove_ansi_escape_sequences(no_args_output.getvalue().strip())

    # Capture output for 'help' command
    help_cmd_output = StringIO()
    sys.stdout = help_cmd_output
    with pytest.raises(SystemExit):
        run(["help"])
    sys.stdout = sys.__stdout__
    help_cmd_text = remove_ansi_escape_sequences(help_cmd_output.getvalue().strip())

    # Capture output for '--help' flag
    help_flag_output = StringIO()
    sys.stdout = help_flag_output
    with pytest.raises(SystemExit):
        run(["--help"])
    sys.stdout = sys.__stdout__
    help_flag_text = remove_ansi_escape_sequences(help_flag_output.getvalue().strip())

    # Assert all outputs are the same
    assert no_args_text == help_cmd_text
    assert help_cmd_text == help_flag_text
    assert no_args_text == help_flag_text
