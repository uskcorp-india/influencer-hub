from unittest.mock import patch, MagicMock
from handler import influencer_handler

@patch('handler.influencer_handler.build_response')
@patch('handler.influencer_handler.db.create_influencer')
@patch('handler.influencer_handler.validator.validate')
def test_create_valid_influencer(mock_validate, mock_create_influencer, mock_build_response):
    influencer = {
        'name': 'Alice Smith',
        'email': 'alice@example.com',
        'phone': '1234567890',
        'platform': 'Instagram',
        'followers': 10000
    }
    mock_validate.return_value = influencer
    mock_create_influencer.return_value = {'id': 'abc123'}
    mock_build_response.return_value = {'message': 'influencer Created Successfully'}
    result = influencer_handler.create(influencer)
    mock_validate.assert_called_once_with(influencer)
    mock_create_influencer.assert_called_once_with(influencer)
    mock_build_response.assert_called_once_with({'id': 'abc123'}, 'influencer Created Successfully')
    assert result == {'message': 'influencer Created Successfully'}

@patch('handler.influencer_handler.build_response')
@patch('handler.influencer_handler.validator.validate')
def test_create_invalid_influencer(mock_validate, mock_build_response):
    influencer = {
        'email': 'invalid-email',
        'followers': -50
    }

    errors = ['Missing required field: name', 'Missing required field: phone', 'Missing required field: platform']
    mock_validate.return_value = {'errors': errors}
    mock_build_response.return_value = {'error': errors, 'status': 400}
    result = influencer_handler.create(influencer)
    mock_validate.assert_called_once_with(influencer)
    mock_build_response.assert_called_once_with(errors, 400)
    assert result == {'error': errors, 'status': 400}

@patch('handler.influencer_handler.build_response')
@patch('handler.influencer_handler.db.find_influencer')
def test_find_influencer_success(mock_find_influencer, mock_build_response):
    influencer_id = 'inf123'
    db_response = {
        'id': influencer_id,
        'name': 'John Doe',
        'email': 'john@example.com'
    }
    expected_response = {
        'data': db_response,
        'message': 'influencer Found Successfully'
    }
    mock_find_influencer.return_value = db_response
    mock_build_response.return_value = expected_response
    response = influencer_handler.find(influencer_id)
    mock_find_influencer.assert_called_once_with(influencer_id)
    mock_build_response.assert_called_once_with(db_response, "influencer Found Successfully")
    assert response['message'] == expected_response['message']
    assert response['data']['id'] == db_response['id']
    assert response['data']['name'] == db_response['name']
    assert response['data']['email'] == db_response['email']

@patch('handler.influencer_handler.build_response')
@patch('handler.influencer_handler.db.find_influencer')
def test_find_influencer_not_found(mock_find_influencer, mock_build_response):
    influencer_id = 'inf999'
    db_response = None
    expected_response = {
        'data': None,
        'message': 'influencer Found Successfully'
    }
    mock_find_influencer.return_value = db_response
    mock_build_response.return_value = expected_response
    response = influencer_handler.find(influencer_id)
    mock_find_influencer.assert_called_once_with(influencer_id)
    mock_build_response.assert_called_once_with(db_response, "influencer Found Successfully")
    assert response['message'] == expected_response['message']
    assert response['data'] == db_response

@patch('handler.influencer_handler.build_response')
@patch('handler.influencer_handler.db.update_influencer')
@patch('handler.influencer_handler.validator.validate')
def test_update_influencer_success(mock_validate, mock_update_influencer, mock_build_response):
    influencer = {
        'id': 'inf123',
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '1234567890',
        'platform': 'Instagram',
        'followers': 1000
    }
    mock_validate.return_value = influencer
    db_response = {'id': 'inf123', 'updated': True}
    mock_update_influencer.return_value = db_response
    expected_response = {'data': db_response, 'message': 'influencer Updated Successfully'}
    mock_build_response.return_value = expected_response
    response = influencer_handler.update(influencer)
    mock_validate.assert_called_once_with(influencer)
    mock_update_influencer.assert_called_once_with(influencer)
    mock_build_response.assert_called_once_with(db_response, 'influencer Updated Successfully')
    assert response == expected_response

@patch('handler.influencer_handler.build_response')
@patch('handler.influencer_handler.validator.validate')
def test_update_influencer_validation_error(mock_validate, mock_build_response):
    influencer = {
        'id': 'inf123',
        'name': '',
        'email': 'invalid-email',
        'phone': '123',
        'platform': '',
        'followers': -5
    }
    validation_errors = ['Name cannot be empty', 'Invalid email format', 'Phone number invalid']
    mock_validate.return_value = {'errors': validation_errors}
    expected_response = {'errors': validation_errors}
    mock_build_response.return_value = expected_response
    response = influencer_handler.update(influencer)
    mock_validate.assert_called_once_with(influencer)
    mock_build_response.assert_called_once_with(validation_errors, 400)
    assert response == expected_response

@patch('handler.influencer_handler.build_response')
@patch('handler.influencer_handler.db.delete_influencer')
def test_delete_influencer_success(mock_delete_influencer, mock_build_response):
    influencer_id = 'inf123'
    db_response = {'id': influencer_id, 'deleted': True}
    expected_response = {'data': db_response, 'message': 'influencer deleted successfully'}
    mock_delete_influencer.return_value = db_response
    mock_build_response.return_value = expected_response
    response = influencer_handler.delete(influencer_id)
    mock_delete_influencer.assert_called_once_with(influencer_id)
    mock_build_response.assert_called_once_with(db_response, message="influencer deleted successfully")
    assert response['message'] == expected_response['message']
    assert response['data']['id'] == db_response['id']

@patch('handler.influencer_handler.build_response')
@patch('handler.influencer_handler.db.delete_influencer')
def test_delete_influencer_failure(mock_delete_influencer, mock_build_response):
    influencer_id = 'inf123'
    db_response = None
    expected_errors = ["Delete operation failed"]
    expected_response = {'errors': expected_errors, 'message': 'Failed to delete influencer'}
    mock_delete_influencer.return_value = db_response
    mock_build_response.return_value = expected_response
    response = influencer_handler.delete(influencer_id)
    mock_delete_influencer.assert_called_once_with(influencer_id)
    mock_build_response.assert_called_once_with(db_response, message="influencer deleted successfully")
    assert response == expected_response

@patch('handler.influencer_handler.build_response')
@patch('handler.influencer_handler.db.find_all_influencers')
def test_find_all_influencers_success(mock_find_all, mock_build_response):
    db_response = [
        {'id': 'inf1', 'name': 'Alice', 'email': 'alice@example.com'},
        {'id': 'inf2', 'name': 'Bob', 'email': 'bob@example.com'}
    ]
    expected_response = {
        'data': db_response,
        'message': 'All influencer Fetched Successfully'
    }

    mock_find_all.return_value = db_response
    mock_build_response.return_value = expected_response
    response = influencer_handler.find_all()
    mock_find_all.assert_called_once()
    mock_build_response.assert_called_once_with(db_response, "All influencer Fetched Successfully")
    assert response['message'] == "All influencer Fetched Successfully"
    assert len(response['data']) == len(db_response)
    assert response['data'][0]['id'] == db_response[0]['id']
    assert response['data'][0]['name'] == db_response[0]['name']
    assert response['data'][0]['email'] == db_response[0]['email']

@patch('handler.influencer_handler.build_response')
@patch('handler.influencer_handler.db.find_all_influencers')
def test_find_all_influencers_failure(mock_find_all, mock_build_response):
    db_response = []
    expected_response = {
        'data': db_response,
        'message': 'No influencers found'
    }
    mock_find_all.return_value = db_response
    mock_build_response.return_value = expected_response
    response = influencer_handler.find_all()
    mock_find_all.assert_called_once()
    mock_build_response.assert_called_once_with(db_response, "All influencer Fetched Successfully")
    assert response['message'] == expected_response['message']
    assert response['data'] == db_response