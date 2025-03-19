"""
Tests for the dotted path completion functionality.
"""

import pytest
from dotcat.data_access import get_dotted_path_completions


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


@pytest.mark.parametrize(
    "lookup_chain, expected_completions, test_description",
    [
        ("", ["company"], "empty_lookup"),
        ("c", ["company"], "single_char_match"),
        (
            "company",
            ["name", "address", "employees", "projects"],
            "exact_match_first_level",
        ),
        ("company.", ["name", "address", "employees", "projects"], "dot_after_company"),
        ("company.n", ["name"], "company_name_partial"),
        (
            "company.address",
            ["street", "city", "zip", "country"],
            "exact_match_second_level",
        ),
        ("company.address.", ["street", "city", "zip", "country"], "dot_after_address"),
        ("company.address.c", ["city", "country"], "address_city_partial"),
        (
            "company.projects.project_alpha",
            ["status", "priority"],
            "exact_match_third_level",
        ),
        ("company.employees.", [], "employees_no_completion"),
        ("company.employees", [], "employees_no_completion"),
        ("nonexistent", [], "nonexistent_key"),
        ("company.nonexistent", [], "nonexistent_nested_key"),
    ],
    ids=[
        "empty_lookup",
        "single_char_match",
        "exact_match_first_level",
        "dot_after_company",
        "company_name_partial",
        "exact_match_second_level",
        "dot_after_address",
        "address_city_partial",
        "exact_match_third_level",
        "employees_no_completion",
        "employees_no_completion_no_dot",
        "nonexistent_key",
        "nonexistent_nested_key",
    ],
)
def test_dotted_path_completions(
    complex_data, lookup_chain, expected_completions, test_description
):
    """Test possible completions for various dotted paths."""
    result = get_dotted_path_completions(complex_data, lookup_chain)
    assert sorted(result) == sorted(
        expected_completions
    ), f"Failed for {test_description}"
