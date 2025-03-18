import pathlib
from unittest.mock import patch

from dotcat.__version__ import get_version_from_toml


def test_get_version_from_toml():
    """Test that get_version_from_toml correctly extracts version from pyproject.toml."""
    # Get the actual version from pyproject.toml
    project_root = pathlib.Path(__file__).parent.parent
    pyproject_path = project_root / "pyproject.toml"

    # This test will fail if pyproject.toml doesn't exist or doesn't have a version
    assert pyproject_path.exists(), "pyproject.toml not found"

    # Get the version using our function
    version = get_version_from_toml()

    # Verify it's not "unknown"
    assert version != "unknown", "Version should not be 'unknown'"

    # Verify it's a string in the format of a version (e.g., "0.9.1")
    assert isinstance(version, str), "Version should be a string"
    assert "." in version, "Version should contain at least one dot"


def test_get_version_from_toml_with_mock():
    """Test get_version_from_toml with a mocked pyproject.toml file."""

    # Mock the open function and toml.load to return our mock content
    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("toml.load", return_value={"project": {"version": "1.2.3"}}),
    ):
        version = get_version_from_toml()
        assert version == "1.2.3"


def test_get_version_from_toml_file_not_found():
    """Test get_version_from_toml when pyproject.toml is not found."""
    with patch("pathlib.Path.exists", return_value=False):
        version = get_version_from_toml()
        assert version == "unknown"


def test_get_version_from_toml_exception():
    """Test get_version_from_toml when an exception occurs."""
    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("toml.load", side_effect=Exception("Test exception")),
    ):
        version = get_version_from_toml()
        assert version == "unknown"
