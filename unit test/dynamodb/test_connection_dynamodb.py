from unittest.mock import patch, MagicMock
from dynamodb import connection
import pytest

REGION = 'ap-south-1'
DYNAMODB = 'dynamodb'

@patch('dynamodb.connection.boto3')
def test_get_connection(mock_boto3):
    mock_resource = MagicMock()
    mock_boto3.resource.return_value = mock_resource
    result = connection.get_connection()
    mock_boto3.resource.assert_called_once_with('dynamodb', region_name='ap-south-1')
    assert result == mock_resource

@patch('dynamodb.connection.boto3')
def test_get_connection_failure(mock_boto3):
    mock_boto3.resource.side_effect = Exception("Failed to connect")
    with pytest.raises(Exception) as exc_info:
        connection.get_connection()
    assert str(exc_info.value) == "Failed to connect"

def test_with_connection_success():
    with patch('dynamodb.connection.get_connection') as mock_get_conn:
        mock_dynamodb = MagicMock()
        mock_get_conn.return_value = mock_dynamodb
        @connection.with_connection
        def sample_func(dynamodb, name):
            return f"Connected to {dynamodb} as {name}"
        result = sample_func("Nithin")
        assert result == f"Connected to {mock_dynamodb} as Nithin"
        mock_get_conn.assert_called_once()
        mock_dynamodb.close.assert_called_once()

def test_with_connection_failure():
    with patch('dynamodb.connection.get_connection') as mock_get_conn, \
         patch('dynamodb.connection.logger') as mock_logger, \
         patch('dynamodb.connection.build_response') as mock_response:
        mock_dynamodb = MagicMock()
        mock_get_conn.return_value = mock_dynamodb
        mock_response.return_value = {
            "statusCode": 500,
            "body": {"error": "Something went wrong"}
        }
        @connection.with_connection
        def error_func(dynamodb):
            raise RuntimeError("Something went wrong")
        result = error_func()
        assert result == {
            "statusCode": 500,
            "body": {"error": "Something went wrong"}
        }
        mock_logger.exception.assert_called_once()
        mock_response.assert_called_once_with(500, {"error": "Something went wrong"})
        mock_dynamodb.close.assert_called_once()