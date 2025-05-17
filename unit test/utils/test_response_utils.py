from utils.response_utils import build_response

def test_build_response_with_valid_data():
    data = {"key": "value"}
    response = build_response(data, "Success")
    assert response == (data, {'message': "Success"})

def test_build_response_with_empty_data():
    response = build_response({}, "Success")
    assert response == ({}, {'message': "Success"})

def test_build_response_with_non_empty_data():
    data = {"key": "value"}
    response = build_response(data, "Success")
    assert response == (data, {'message': "Success"})

def test_build_response_with_none():
    response = build_response(None, "Success")
    assert response == (None, {'message': "Success"})

def test_build_response_with_non_none_data():
    data = "Test data"  # Non-None data
    response = build_response(data, "Success")
    assert response == (data, {'message': "Success"})

def test_build_response_with_list():
    data = [1, 2, 3]
    response = build_response(data, "Success")
    assert response == (data, {'message': "Success"})

def test_build_response_with_non_list_data():
    data = {"key": "value"}
    response = build_response(data, "Success")
    assert response == (data, {'message': "Success"})

def test_build_response_with_string():
    response = build_response("test_string", "String received")
    assert response == ("test_string", {'message': "String received"})