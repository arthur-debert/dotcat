import pytest
import yaml
from dotcat.dotcat import format_output
from datetime import date

@pytest.fixture
def complex_data():
    with open("tests/fixtures/complex.yaml", 'r') as file:
        return yaml.safe_load(file)

def test_complex_output_raw(complex_data):
    output = format_output(complex_data, 'raw')
    expected_output = str(complex_data)  # Directly convert the data to string
    assert output.strip() == expected_output.strip()

def test_complex_output_formatted(complex_data):
    output = format_output(complex_data, 'formatted')
    expected_output = '''{
    "name": "Example",
    "age": 30,
    "height": 5.9,
    "birthdate": "1990-01-01",
    "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "zip": 12345
    },
    "phones": [
        {
            "type": "home",
            "number": "555-555-5555"
        },
        {
            "type": "work",
            "number": "555-555-5556"
        }
    ],
    "emails": [
        {
            "personal": "example@example.com"
        },
        {
            "work": "work@example.com"
        }
    ],
    "projects": [
        {
            "name": "Project A",
            "tasks": [
                {
                    "task": "Task 1",
                    "due": "2023-01-01"
                },
                {
                    "task": "Task 2",
                    "due": "2023-02-01"
                }
            ]
        },
        {
            "name": "Project B",
            "tasks": [
                {
                    "task": "Task 3",
                    "due": "2023-03-01"
                },
                {
                    "task": "Task 4",
                    "due": "2023-04-01"
                }
            ]
        }
    ]
}'''
    assert output.strip() == expected_output.strip()

def test_complex_output_json(complex_data):
    output = format_output(complex_data, 'json')
    expected_output = '''{
    "name": "Example",
    "age": 30,
    "height": 5.9,
    "birthdate": "1990-01-01",
    "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "zip": 12345
    },
    "phones": [
        {
            "type": "home",
            "number": "555-555-5555"
        },
        {
            "type": "work",
            "number": "555-555-5556"
        }
    ],
    "emails": [
        {
            "personal": "example@example.com"
        },
        {
            "work": "work@example.com"
        }
    ],
    "projects": [
        {
            "name": "Project A",
            "tasks": [
                {
                    "task": "Task 1",
                    "due": "2023-01-01"
                },
                {
                    "task": "Task 2",
                    "due": "2023-02-01"
                }
            ]
        },
        {
            "name": "Project B",
            "tasks": [
                {
                    "task": "Task 3",
                    "due": "2023-03-01"
                },
                {
                    "task": "Task 4",
                    "due": "2023-04-01"
                }
            ]
        }
    ]
}'''
    expected_output = '''{"name": "Example", "age": 30, "height": 5.9, "birthdate": "1990-01-01", "address": {"street": "123 Main St", "city": "Anytown", "zip": 12345}, "phones": [{"type": "home", "number": "555-555-5555"}, {"type": "work", "number": "555-555-5556"}], "emails": [{"personal": "example@example.com"}, {"work": "work@example.com"}], "projects": [{"name": "Project A", "tasks": [{"task": "Task 1", "due": "2023-01-01"}, {"task": "Task 2", "due": "2023-02-01"}]}, {"name": "Project B", "tasks": [{"task": "Task 3", "due": "2023-03-01"}, {"task": "Task 4", "due": "2023-04-01"}]}]}'''

    assert output.strip() == expected_output.strip()

def test_complex_output_yaml(complex_data):
    output = format_output(complex_data, 'yaml')
    expected_output = '''address:
  city: Anytown
  street: 123 Main St
  zip: 12345
age: 30
birthdate: 1990-01-01
emails:
- personal: example@example.com
- work: work@example.com
height: 5.9
name: Example
phones:
- number: 555-555-5555
  type: home
- number: 555-555-5556
  type: work
projects:
- name: Project A
  tasks:
  - due: 2023-01-01
    task: Task 1
  - due: 2023-02-01
    task: Task 2
- name: Project B
  tasks:
  - due: 2023-03-01
    task: Task 3
  - due: 2023-04-01
    task: Task 4
'''
    assert output.strip() == expected_output.strip()

def test_complex_output_toml(complex_data):
    output = format_output(complex_data, 'toml')
    expected_output = '''name = "Example"
age = 30
height = 5.9
birthdate = 1990-01-01

[[phones]]
type = "home"
number = "555-555-5555"

[[phones]]
type = "work"
number = "555-555-5556"

[[emails]]
personal = "example@example.com"

[[emails]]
work = "work@example.com"

[[projects]]
name = "Project A"

[[projects.tasks]]
task = "Task 1"
due = 2023-01-01

[[projects.tasks]]
task = "Task 2"
due = 2023-02-01

[[projects]]
name = "Project B"

[[projects.tasks]]
task = "Task 3"
due = 2023-03-01

[[projects.tasks]]
task = "Task 4"
due = 2023-04-01

[address]
street = "123 Main St"
city = "Anytown"
zip = 12345
'''

    # Normalize both outputs by removing extra newlines:
    output = '\n'.join([line for line in output.splitlines() if line.strip()])
    expected_output = '\n'.join([line for line in expected_output.splitlines() if line.strip()])

    assert output == expected_output


def test_complex_output_ini(complex_data):
    output = format_output(complex_data, 'ini')
    expected_output = '''[default]
name = Example
age = 30
height = 5.9
birthdate = 1990-01-01

[projects]
name = Project A
tasks = [{'task': 'Task 1', 'due': '2023-01-01'}, {'task': 'Task 2', 'due': '2023-02-01'}]
name = Project B
tasks = [{'task': 'Task 3', 'due': '2023-03-01'}, {'task': 'Task 4', 'due': '2023-04-01'}]

[phones]
number = 555-555-5555
type = home
number = 555-555-5556
type = work

[address]
city = Anytown
street = 123 Main St
zip = 12345

[emails]
personal = example@example.com
work = work@example.com


'''
    assert output.strip() == expected_output.strip()