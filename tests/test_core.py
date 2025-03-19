"""
Tests for the core module functions.
"""

import pytest
from unittest.mock import patch

from dotcat.core import (
    is_likely_dot_path,
    process_file,
    lookup_value,
    format_value,
)


def test_is_likely_dot_path():
    """Test that dot paths are correctly identified."""
    # Test a dot path
    assert is_likely_dot_path("config.settings") is True

    # Test a file path that exists (mocked)
    with patch("os.path.exists", return_value=True):
        assert is_likely_dot_path("config.json") is False

    # Test a string without dots
    assert is_likely_dot_path("config") is False


def test_process_file():
    """Test that files are processed correctly."""
    # Test with a valid file
    with patch("dotcat.core.parse_file", return_value={"key": "value"}):
        result = process_file("config.json")
        assert result == {"key": "value"}

    # Test with a file not found error
    with patch(
        "dotcat.core.parse_file", side_effect=FileNotFoundError("File not found")
    ):
        with pytest.raises(FileNotFoundError) as excinfo:
            process_file("nonexistent.json")
        assert "File not found" in str(excinfo.value)

    # Test with a value error (empty file)
    with patch("dotcat.core.parse_file", side_effect=ValueError("File is empty")):
        with pytest.raises(ValueError) as excinfo:
            process_file("empty.json")
        assert "File is empty" in str(excinfo.value)

    # Test with a value error (unable to parse)
    with patch(
        "dotcat.core.parse_file", side_effect=ValueError("Unable to parse file")
    ):
        with pytest.raises(ValueError) as excinfo:
            process_file("malformed.json")
        assert "Unable to parse file" in str(excinfo.value)


def test_lookup_value():
    """Test that values are looked up correctly."""
    # Test with a valid key
    with patch("dotcat.core.from_dotted_path", return_value="value"):
        result = lookup_value({"key": "value"}, "key")
        assert result == "value"

    # Test with a key not found error
    with patch(
        "dotcat.core.from_dotted_path",
        side_effect=KeyError("key 'nonexistent' not found"),
    ):
        with pytest.raises(KeyError) as excinfo:
            lookup_value({"key": "value"}, "nonexistent")
        assert "nonexistent" in str(excinfo.value)


def test_format_value():
    """Test that values are formatted correctly."""
    # Test with raw format
    with patch("dotcat.core.format_output", return_value="value"):
        result = format_value("value", "raw")
        assert result == "value"

    # Test with json format
    with patch("dotcat.core.format_output", return_value='{"key": "value"}'):
        result = format_value({"key": "value"}, "json")
        assert result == '{"key": "value"}'

    # Test with yaml format
    with patch("dotcat.core.format_output", return_value="key: value"):
        result = format_value({"key": "value"}, "yaml")
        assert result == "key: value"
