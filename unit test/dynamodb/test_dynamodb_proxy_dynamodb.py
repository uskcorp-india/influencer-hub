from unittest.mock import patch
import dynamodb.dynamodb_proxy as dynamodb_proxy
import pytest

@patch('dynamodb.dynamodb_proxy.customer_dao.create')
def test_create_customer(mock_create):
    customer_data = {'id': '1', 'name': 'Nithin'}
    mock_create.return_value = {'id': '1', 'name': 'Nithin', 'status': 'success'}
    response = dynamodb_proxy.create_customer(customer_data)
    mock_create.assert_called_once_with(customer_data)
    assert response['id'] == customer_data['id']
    assert response['name'] == customer_data['name']
    assert response['status'] == 'success'

@patch('dynamodb.dynamodb_proxy.customer_dao.create')
def test_create_customer_invalid(mock_create):
    customer_data = {'id': '', 'name': ''}
    mock_create.side_effect = Exception("Invalid customer data")
    with pytest.raises(Exception) as exc_info:
        dynamodb_proxy.create_customer(customer_data)
    mock_create.assert_called_once_with(customer_data)
    assert str(exc_info.value) == "Invalid customer data"

@patch('dynamodb.dynamodb_proxy.customer_dao.update')
def test_update_customer(mock_update):
    customer_data = {'id': '1', 'name': 'Updated'}
    mock_update.return_value = {'id': '1', 'name': 'Updated', 'status': 'updated'}
    response = dynamodb_proxy.update_customer(customer_data)
    mock_update.assert_called_once_with(customer_data)
    assert response['id'] == customer_data['id']
    assert response['name'] == customer_data['name']
    assert response['status'] == 'updated'

@patch('dynamodb.dynamodb_proxy.customer_dao.update')
def test_update_customer_invalid(mock_update):
    customer_data = {'id': '', 'name': ''}  # Invalid input
    mock_update.side_effect = Exception("Invalid customer data")
    with pytest.raises(Exception) as exc_info:
        dynamodb_proxy.update_customer(customer_data)
    mock_update.assert_called_once_with(customer_data)
    assert str(exc_info.value) == "Invalid customer data"

@patch('dynamodb.dynamodb_proxy.customer_dao.delete')
def test_delete_customer(mock_delete):
    customer_id = '1'
    mock_delete.return_value = {'status': 'deleted'}
    response = dynamodb_proxy.delete_customer(customer_id)
    mock_delete.assert_called_once_with(customer_id)
    assert response['status'] == mock_delete.return_value['status']

@patch('dynamodb.dynamodb_proxy.customer_dao.delete')
def test_delete_customer_invalid(mock_delete):
    customer_id = '999'
    mock_delete.return_value = {'status': 'error', 'message': 'Customer not found'}
    response = dynamodb_proxy.delete_customer(customer_id)
    mock_delete.assert_called_once_with(customer_id)
    assert response['status'] == mock_delete.return_value['status']
    assert response['message'] == mock_delete.return_value['message']

@patch('dynamodb.dynamodb_proxy.customer_dao.find')
def test_find_customer_valid(mock_find):
    customer_id = '123'
    mock_customer = {
        'customer_id': '123',
        'name': 'Alice',
        'email': 'alice@example.com'
    }
    mock_find.return_value = mock_customer
    response = dynamodb_proxy.find_customer(customer_id)
    mock_find.assert_called_once_with(customer_id)
    assert response['customer_id'] == mock_customer['customer_id']
    assert response['name'] == mock_customer['name']
    assert response['email'] == mock_customer['email']

@patch('dynamodb.dynamodb_proxy.customer_dao.find')
def test_find_customer_not_found(mock_find):
    customer_id = '999'  # Non-existent customer ID
    mock_find.return_value = None
    response = dynamodb_proxy.find_customer(customer_id)
    mock_find.assert_called_once_with(customer_id)
    assert response is None or isinstance(response, type(None))  # Type-based assertion

@patch('dynamodb.dynamodb_proxy.customer_dao.find_all')
def test_find_all_customers(mock_find_all):
    mock_customers = [
        {'customer_id': '101', 'name': 'Alice', 'email': 'alice@example.com'},
        {'customer_id': '102', 'name': 'Bob', 'email': 'bob@example.com'}
    ]
    mock_find_all.return_value = mock_customers
    response = dynamodb_proxy.find_all_customers()
    mock_find_all.assert_called_once()
    assert isinstance(response, list)
    assert len(response) == 2
    assert response[0]['customer_id'] == mock_customers[0]['customer_id']
    assert response[1]['email'] == mock_customers[1]['email']

@patch('dynamodb.dynamodb_proxy.customer_dao.find_all')
def test_find_all_customers_empty(mock_find_all):
    mock_find_all.return_value = []
    response = dynamodb_proxy.find_all_customers()
    mock_find_all.assert_called_once()
    assert isinstance(response, list)
    assert len(response) == 0