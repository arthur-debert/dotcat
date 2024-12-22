import pytest
import yaml
from dotcat.dotcat import access_list, from_attr_chain

@pytest.fixture
def list_data():
    with open("tests/fixtures/list.yaml", 'r') as file:
        return yaml.safe_load(file)

def test_access_list_single_item(list_data):
    result = access_list(list_data['foo'], 'bar', '2')
    expected = list_data['foo']['bar'][2]
    assert result == expected

def test_access_list_slice(list_data):
    result = access_list(list_data['foo'], 'bar', '2:4')
    expected = list_data['foo']['bar'][2:4]
    assert result == expected

def test_access_list_start_to_index(list_data):
    result = access_list(list_data['foo'], 'bar', ':3')
    expected = list_data['foo']['bar'][:3]
    assert result == expected

def test_access_list_index_to_end(list_data):
    result = access_list(list_data['foo'], 'bar', '3:-1')
    expected = list_data['foo']['bar'][3:-1]
    assert result == expected

def test_list_access_single_item(list_data):
    result = from_attr_chain(list_data, 'foo.bar@2')
    expected = list_data['foo']['bar'][2]
    assert result == expected

def test_list_access_slice(list_data):
    result = from_attr_chain(list_data, 'foo.bar@2:4')
    expected = list_data['foo']['bar'][2:4]
    assert result == expected

def test_list_access_start_to_index(list_data):
    result = from_attr_chain(list_data, 'foo.bar@:3')
    expected = list_data['foo']['bar'][:3]
    assert result == expected

def test_list_access_index_to_end(list_data):
    result = from_attr_chain(list_data, 'foo.bar@3:-1')
    expected = list_data['foo']['bar'][3:-1]
    assert result == expected
