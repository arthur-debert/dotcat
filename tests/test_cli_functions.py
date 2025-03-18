"""
Tests for the individual functions in the cli module.
"""

import pytest
from io import StringIO
from unittest.mock import patch

from dotcat.cli import (
    handle_version_flag,
    handle_special_case_arguments,
    validate_required_arguments,
    process_and_display_result,
)
from dotcat.core import is_likely_dot_path
from dotcat.__version__ import __version__
from dotcat.help_text import USAGE


def test_handle_version_flag():
    """Test that the version flag is handled correctly."""
    with patch("sys.stdout", new=StringIO()) as fake_out:
        result = handle_version_flag(True)
        assert result is True
        assert fake_out.getvalue().strip() == f"dotcat version {__version__}"

    with patch("sys.stdout", new=StringIO()) as fake_out:
        result = handle_version_flag(False)
        assert result is False
        assert fake_out.getvalue().strip() == ""


def test_handle_special_case_arguments():
    """Test that special case arguments are handled correctly."""
    # Test case where filename looks like a dotted-path
    filename, lookup_chain = handle_special_case_arguments(
        "config.settings", None, ["config.settings"]
    )
    assert filename is None
    assert lookup_chain == "config.settings"

    # Test case where filename doesn't look like a dotted-path
    filename, lookup_chain = handle_special_case_arguments("config", None, ["config"])
    assert filename == "config"
    assert lookup_chain is None

    # Test case with both arguments provided
    filename, lookup_chain = handle_special_case_arguments(
        "config.json", "settings", ["config.json", "settings"]
    )
    assert filename == "config.json"
    assert lookup_chain == "settings"


def test_is_likely_dot_path():
    """Test that dot paths are correctly identified."""
    # Test a dot path
    assert is_likely_dot_path("config.settings") is True

    # Test a file path that exists (mocked)
    with patch("os.path.exists", return_value=True):
        assert is_likely_dot_path("config.json") is False

    # Test a string without dots
    assert is_likely_dot_path("config") is False


def test_validate_required_arguments():
    """Test that required arguments are validated correctly."""
    # Test case where both arguments are provided
    validate_required_arguments(
        "config.json", "settings", ["config.json", "settings"]
    )  # Should not raise

    # Test case where file is provided but dotted-path is missing
    with patch("os.path.exists", return_value=True):
        with patch("sys.stdout", new=StringIO()):
            with pytest.raises(SystemExit) as excinfo:
                validate_required_arguments("config.json", None, ["config.json"])
            assert excinfo.value.code == 2

    # Test case where dotted-path is provided but file is missing
    with patch("sys.stdout", new=StringIO()):
        with pytest.raises(SystemExit) as excinfo:
            validate_required_arguments(None, "config.settings", ["config.settings"])
        assert excinfo.value.code == 2

    # Test case where both arguments are missing
    with patch("sys.stdout", new=StringIO()) as fake_out:
        with pytest.raises(SystemExit) as excinfo:
            validate_required_arguments(None, None, [])
        assert excinfo.value.code == 2
        assert USAGE in fake_out.getvalue()


def test_process_and_display_result():
    """Test that process_and_display_result works correctly."""
    # Test with a valid file and key
    with patch("dotcat.cli.process_file", return_value={"key": "value"}):
        with patch("dotcat.cli.lookup_value", return_value="value"):
            with patch("dotcat.cli.format_value", return_value="value"):
                with patch("sys.stdout", new=StringIO()) as fake_out:
                    process_and_display_result("config.json", "key", "raw")
                    assert fake_out.getvalue().strip() == "value"

    # Test with a file not found error
    with patch(
        "dotcat.cli.process_file", side_effect=FileNotFoundError("File not found")
    ):
        with patch("sys.stdout", new=StringIO()):
            with pytest.raises(SystemExit) as excinfo:
                process_and_display_result("nonexistent.json", "key", "raw")
            assert excinfo.value.code == 3

    # Test with a parsing error
    with patch(
        "dotcat.cli.process_file", side_effect=ValueError("Unable to parse file")
    ):
        with patch("sys.stdout", new=StringIO()):
            with pytest.raises(SystemExit) as excinfo:
                process_and_display_result("malformed.json", "key", "raw")
            assert excinfo.value.code == 4

    # Test with a key not found error
    with patch("dotcat.cli.process_file", return_value={"key": "value"}):
        with patch(
            "dotcat.cli.lookup_value",
            side_effect=KeyError("key 'nonexistent' not found"),
        ):
            with patch("sys.stdout", new=StringIO()):
                with pytest.raises(SystemExit) as excinfo:
                    process_and_display_result("config.json", "nonexistent", "raw")
                assert excinfo.value.code == 5
