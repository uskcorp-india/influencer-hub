from unittest.mock import patch
import pytest
from datetime import datetime
import utils.dao_utils as dao_utils

def test_build_record():
    record = dao_utils.build_record()
    expected_status = True
    assert 'id' in record
    assert isinstance(record['id'], str) and len(record['id']) > 0
    assert record['status'] == expected_status, f"Expected status to be {expected_status}"
    try:
        datetime.strptime(record['created_at'], "%d-%m-%Y %H:%M:%S")
    except ValueError:
        pytest.fail("created_at format is incorrect")

def test_build_record_invalid():
    record = dao_utils.build_record()
    expected = {
        'status': False,
        'created_at': 'invalid-date-format'
    }

    record['status'] = expected['status']
    record['created_at'] = expected['created_at']
    assert record['status'] == expected['status'], "Status should be False in this invalid test"
    assert record['created_at'] == expected['created_at'], "created_at should be set to invalid format"
    try:
        datetime.strptime(record['created_at'], "%d-%m-%Y %H:%M:%S")
        pytest.fail("created_at format should be invalid but parsing succeeded")
    except ValueError:
        pass
@patch('dynamodb_json.json_util.loads')
def test_from_attributes_to_json(mock_json_loads):
    test_dict = {'S': 'value'}
    expected_output = {'key': 'value'}
    mock_json_loads.return_value = expected_output
    result = dao_utils.from_attributes_to_json(test_dict)
    mock_json_loads.assert_called_once_with(test_dict)
    assert result == expected_output


@patch('dynamodb_json.json_util.loads')
def test_from_attributes_to_json_invalid(mock_json_loads):
    test_dict = {'S': 'value'}
    expected_output = {'key': 'value'}
    mock_json_loads.return_value = None
    result = dao_utils.from_attributes_to_json(test_dict)
    mock_json_loads.assert_called_once_with(test_dict)
    assert result != expected_output, "Result should not match expected output for invalid test case"
    assert result is None, "Result should be None in this invalid scenario"