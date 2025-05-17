from unittest.mock import patch
import handler.customer_handler as customer_handler

@patch('handler.customer_handler.build_response')
@patch('handler.customer_handler.db.create_customer')
@patch('handler.customer_handler.validator.validate')
def test_create_customer_valid(mock_validate, mock_create_customer, mock_build_response):
    customer = {'customer_id': '123', 'name': 'Alice'}
    mock_validate.return_value = customer
    db_response = {'customer_id': '123', 'name': 'Alice', 'status': 'created'}
    mock_create_customer.return_value = db_response
    mock_build_response.return_value = db_response
    response = customer_handler.create(customer)
    mock_validate.assert_called_once_with(customer)
    mock_create_customer.assert_called_once_with(customer)
    mock_build_response.assert_called_once_with(db_response, 'customer Created Successfully')
    assert response['customer_id'] == db_response['customer_id']
    assert response['name'] == db_response['name']
    assert response['status'] == db_response['status']

@patch('handler.customer_handler.build_response')
@patch('handler.customer_handler.validator.validate')
def test_create_customer_invalid(mock_validate, mock_build_response):
    customer = {'customer_id': '', 'name': ''}
    validation_errors = {'errors': {'customer_id': 'Customer ID is required', 'name': 'Name is required'}}
    mock_validate.return_value = validation_errors
    mock_build_response.return_value = validation_errors['errors']
    response = customer_handler.create(customer)
    mock_validate.assert_called_once_with(customer)
    mock_build_response.assert_called_once_with(validation_errors['errors'], 400)
    assert 'customer_id' in response
    assert 'name' in response
    assert response['customer_id'] == validation_errors['errors']['customer_id']
    assert response['name'] == validation_errors['errors']['name']

@patch('handler.customer_handler.build_response')
@patch('handler.customer_handler.db.find_customer')
def test_find_customer_valid(mock_find_customer, mock_build_response):
    customer_id = '123'
    mock_response = {'customer_id': '123', 'name': 'Alice', 'email': 'alice@example.com'}
    mock_find_customer.return_value = mock_response
    mock_build_response.return_value = mock_response
    response = customer_handler.find(customer_id)
    mock_find_customer.assert_called_once_with(customer_id)
    mock_build_response.assert_called_once_with(mock_response, "customer Found Successfully")
    assert response['customer_id'] == mock_response['customer_id']
    assert response['name'] == mock_response['name']
    assert response['email'] == mock_response['email']

@patch('handler.customer_handler.build_response')
@patch('handler.customer_handler.db.find_customer')
def test_find_customer_invalid(mock_find_customer, mock_build_response):
    customer_id = '999'
    mock_find_customer.return_value = None
    error_response = {'error': 'Customer not found'}
    mock_build_response.return_value = error_response
    response = customer_handler.find(customer_id)
    mock_find_customer.assert_called_once_with(customer_id)
    mock_build_response.assert_called_once_with(None, "customer Found Successfully")
    assert response == error_response

@patch('handler.customer_handler.build_response')
@patch('handler.customer_handler.db.update_customer')
@patch('handler.customer_handler.validator.validate')
def test_update_customer_valid(mock_validate, mock_update_customer, mock_build_response):
    customer = {'customer_id': '123', 'name': 'Alice'}
    mock_validate.return_value = customer
    db_response = {'customer_id': '123', 'name': 'Alice', 'status': 'updated'}
    mock_update_customer.return_value = db_response
    mock_build_response.return_value = db_response
    response = customer_handler.update(customer)
    mock_validate.assert_called_once_with(customer)
    mock_update_customer.assert_called_once_with(customer)
    mock_build_response.assert_called_once_with(db_response, 'Customer Updated Successfully')
    assert response['customer_id'] == db_response['customer_id']
    assert response['name'] == db_response['name']
    assert response['status'] == db_response['status']

@patch('handler.customer_handler.build_response')
@patch('handler.customer_handler.validator.validate')
def test_update_customer_invalid(mock_validate, mock_build_response):
    customer = {'customer_id': '', 'name': ''}  # Invalid customer data
    validation_errors = {'errors': {'customer_id': 'Required', 'name': 'Required'}}
    mock_validate.return_value = validation_errors
    mock_build_response.return_value = validation_errors['errors']
    response = customer_handler.update(customer)
    mock_validate.assert_called_once_with(customer)
    mock_build_response.assert_called_once_with(validation_errors['errors'], 400)
    assert 'customer_id' in response
    assert 'name' in response
    assert response['customer_id'] == validation_errors['errors']['customer_id']
    assert response['name'] == validation_errors['errors']['name']

@patch('handler.customer_handler.build_response')
@patch('handler.customer_handler.db.delete_customer')
def test_delete_customer_valid(mock_delete_customer, mock_build_response):
    customer_id = '123'
    mock_response = {'customer_id': '123', 'status': 'deleted'}
    mock_delete_customer.return_value = mock_response
    mock_build_response.return_value = mock_response
    response = customer_handler.delete(customer_id)
    mock_delete_customer.assert_called_once_with(customer_id)
    mock_build_response.assert_called_once_with(mock_response, message="customer deleted successfully")
    assert response['customer_id'] == mock_response['customer_id']
    assert response['status'] == mock_response['status']

@patch('handler.customer_handler.build_response')
@patch('handler.customer_handler.db.delete_customer')
def test_delete_customer_invalid(mock_delete_customer, mock_build_response):
    customer_id = '999'
    mock_response = {'error': 'Customer not found'}
    mock_delete_customer.return_value = mock_response
    mock_build_response.return_value = mock_response
    response = customer_handler.delete(customer_id)
    mock_delete_customer.assert_called_once_with(customer_id)
    mock_build_response.assert_called_once_with(mock_response, message="customer deleted successfully")
    assert 'error' in response
    assert response['error'] == mock_response['error']

@patch('handler.customer_handler.build_response')
@patch('handler.customer_handler.db.find_all_customers')
def test_find_all_customers_valid(mock_find_all_customers, mock_build_response):
    mock_customers = [
        {'customer_id': '101', 'name': 'Alice', 'email': 'alice@example.com'},
        {'customer_id': '102', 'name': 'Bob', 'email': 'bob@example.com'}
    ]
    mock_find_all_customers.return_value = mock_customers
    mock_build_response.return_value = mock_customers
    response = customer_handler.find_all()
    mock_find_all_customers.assert_called_once()
    mock_build_response.assert_called_once_with(mock_customers, "All Customers Fetched Successfully")
    assert response[0]['customer_id'] == mock_customers[0]['customer_id']
    assert response[0]['name'] == mock_customers[0]['name']
    assert response[0]['email'] == mock_customers[0]['email']
    assert response[1]['customer_id'] == mock_customers[1]['customer_id']
    assert response[1]['name'] == mock_customers[1]['name']
    assert response[1]['email'] == mock_customers[1]['email']

@patch('handler.customer_handler.build_response')
@patch('handler.customer_handler.db.find_all_customers')
def test_find_all_customers_invalid(mock_find_all_customers, mock_build_response):
    mock_customers = []
    mock_find_all_customers.return_value = mock_customers
    mock_build_response.return_value = mock_customers
    response = customer_handler.find_all()
    mock_find_all_customers.assert_called_once()
    mock_build_response.assert_called_once_with(mock_customers, "All Customers Fetched Successfully")
    assert isinstance(response, list)
    assert len(response) == 0