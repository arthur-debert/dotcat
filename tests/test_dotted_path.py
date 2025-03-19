"""
Tests for the dotted path access functionality.
"""

import pytest
import yaml
from dotcat.data_access import from_dotted_path


@pytest.fixture
def list_data():
    with open("tests/fixtures/list.yaml", "r") as file:
        return yaml.safe_load(file)


@pytest.fixture
def nested_data():
    return {"python": {"editor": {"tabSize": 4}}}


@pytest.fixture
def complex_data():
    return {
        "company": {
            "name": "TechCorp",
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "zip": "12345",
                "country": "USA",
            },
            "employees": [
                {"id": 101, "name": "Alice", "title": "Developer"},
                {"id": 102, "name": "Bob", "title": "Engineer"},
                {"id": 103, "name": "Charlie", "title": "Manager"},
            ],
            "projects": {
                "project_alpha": {"status": "active", "priority": "high"},
                "project_beta": {"status": "pending", "priority": "medium"},
            },
        }
    }


# Basic nested path access test (from JSON/YAML tests)
def test_basic_nested_path(nested_data):
    result = from_dotted_path(nested_data, "python.editor.tabSize")
    assert result == 4


# Parameterized tests for list access
@pytest.mark.parametrize(
    "dotted_path, expected_result, test_description",
    [
        ("foo.bar@2", lambda data: data["foo"]["bar"][2], "single_item"),
        ("foo.bar@2:4", lambda data: data["foo"]["bar"][2:4], "slice"),
        ("foo.bar@:3", lambda data: data["foo"]["bar"][:3], "start_to_index"),
        ("foo.bar@3:-1", lambda data: data["foo"]["bar"][3:-1], "index_to_end"),
    ],
    ids=[
        "single_index",
        "slice_with_start_and_end",
        "slice_from_start",
        "slice_to_end",
    ],
)
def test_list_access(list_data, dotted_path, expected_result, test_description):
    """Test accessing list elements using various access patterns."""
    result = from_dotted_path(list_data, dotted_path)
    expected = expected_result(list_data)
    assert result == expected, f"Failed for {test_description}"


# Key error test
def test_key_error():
    data = {"python": {"editor": {"tabSize": 4}}}
    with pytest.raises(KeyError) as excinfo:
        from_dotted_path(data, "python.editor.unknownKey")
    assert "unknownKey" in str(excinfo.value)


@pytest.mark.parametrize(
    "dotted_path, expected_result, test_description",
    [
        ("company.name", lambda data: data["company"]["name"], "company_name"),
        (
            "company.address.city",
            lambda data: data["company"]["address"]["city"],
            "company_address_city",
        ),
        (
            "company.projects.project_alpha.status",
            lambda data: data["company"]["projects"]["project_alpha"]["status"],
            "project_alpha_status",
        ),
    ],
    ids=["company_name", "company_address_city", "project_alpha_status"],
)
def test_complex_data_access(
    complex_data, dotted_path, expected_result, test_description
):
    """Test accessing complex data structures using dotted paths."""
    result = from_dotted_path(complex_data, dotted_path)
    expected = expected_result(complex_data)
    assert result == expected, f"Failed for {test_description}"
