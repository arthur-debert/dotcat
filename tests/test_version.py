import pathlib

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
