from validator.customer_validator import validate

def test_validate_with_valid_customer():
    customer = {
        'firstname': 'John',
        'lastname': 'Doe',
        'phone': '1234567890',
        'email': 'john.doe@example.com',
        'house_no': '12A',
        'street': 'Main St',
        'status': True,
        'id': '1234',
        'created_at': '2023-01-01',
        'updated_at': '2023-01-02',
        'address': '12A, Main St',
        'dob': '1990-01-01',
        'gender': 'Male',
        'alias': 'JD'
    }
    result = validate(customer)
    assert 'errors' not in result
    assert result['firstname'] == customer['firstname']
    assert result['lastname'] == customer['lastname']
    assert result['phone'] == customer['phone']
    assert result['email'] == customer['email']
    assert result['house_no'] == customer['house_no']
    assert result['street'] == customer['street']
    assert result['status'] == customer['status']
    assert result['id'] == customer['id']
    assert result['created_at'] == customer['created_at']
    assert result['updated_at'] == customer['updated_at']
    assert result['address'] == customer['address']
    assert result['dob'] == customer['dob']
    assert result['gender'] == customer['gender']
    assert result['alias'] == customer['alias']

def test_validate_with_all_required_fields():
    customer = {
        'firstname': 'John',
        'lastname': 'Doe',
        'phone': '1234567890',
        'email': 'john.doe@example.com',
        'house_no': '12B',
        'street': 'Main Street',
        'status': True
    }
    result = validate(customer)
    assert 'errors' not in result
    assert result['firstname'] == customer['firstname']
    assert result['lastname'] == customer['lastname']
    assert result['phone'] == customer['phone']
    assert result['email'] == customer['email']
    assert result['house_no'] == customer['house_no']
    assert result['street'] == customer['street']
    assert result['status'] == customer['status']

def test_validate_with_missing_required_fields():
    customer = {
        'firstname': 'John',
        'email': 'john.doe@example.com'
    }
    result = validate(customer)
    assert 'errors' in result
    assert any("Missing required field: lastname" in e for e in result['errors'])
    assert any("Missing required field: phone" in e for e in result['errors'])
    assert any("Missing required field: house_no" in e for e in result['errors'])
    assert any("Missing required field: street" in e for e in result['errors'])

def test_validate_with_invalid_customer():
    customer = {
        'firstname': '',
        'lastname': '',
        'phone': '12345',
        'email': 'invalid-email',
        'house_no': '',
        'street': '',
        'status': 'not_boolean'
    }
    result = validate(customer)
    assert 'errors' in result
    assert any("Field 'firstname' should be a non-empty string" in e for e in result['errors'])
    assert any("Field 'lastname' should be a non-empty string" in e for e in result['errors'])
    assert any("Phone number must be a 10-digit number" in e for e in result['errors'])
    assert any("Invalid email format" in e for e in result['errors'])
    assert any("Field 'house number' should be a non-empty string" in e for e in result['errors'])
    assert any("Field 'street' should be a non-empty string" in e for e in result['errors'])
    assert any("Field 'status' should be a boolean" in e for e in result['errors'])

def test_valid_and_invalid():
    valid_customer = {
        'firstname': 'John',
        'lastname': 'Doe',
        'phone': '1234567890',
        'email': 'john.doe@example.com',
        'house_no': '12A',
        'street': 'Main St',
        'status': True,
        'id': '1234',
        'created_at': '2023-01-01',
        'updated_at': '2023-01-02',
        'address': '12A, Main St',
        'dob': '1990-01-01',
        'gender': 'Male',
        'alias': 'JD'
    }
    valid_result = validate(valid_customer)
    assert 'errors' not in valid_result
    assert valid_result['firstname'] == valid_customer['firstname']
    assert valid_result['lastname'] == valid_customer['lastname']
    assert valid_result['phone'] == valid_customer['phone']
    assert valid_result['email'] == valid_customer['email']
    assert valid_result['house_no'] == valid_customer['house_no']
    assert valid_result['street'] == valid_customer['street']
    assert valid_result['status'] == valid_customer['status']
    assert valid_result['id'] == valid_customer['id']
    assert valid_result['created_at'] == valid_customer['created_at']
    assert valid_result['updated_at'] == valid_customer['updated_at']
    assert valid_result['address'] == valid_customer['address']
    assert valid_result['dob'] == valid_customer['dob']
    assert valid_result['gender'] == valid_customer['gender']
    assert valid_result['alias'] == valid_customer['alias']
    invalid_customer = {
        'firstname': '',
        'lastname': '',
        'phone': '12345',
        'email': 'invalid-email',
        'house_no': '',
        'street': '',
        'status': 'not_boolean'
    }
    invalid_result = validate(invalid_customer)
    assert 'errors' in invalid_result
    assert any("Field 'firstname' should be a non-empty string" in e for e in invalid_result['errors'])
    assert any("Field 'lastname' should be a non-empty string" in e for e in invalid_result['errors'])
    assert any("Phone number must be a 10-digit number" in e for e in invalid_result['errors'])
    assert any("Invalid email format" in e for e in invalid_result['errors'])
    assert any("Field 'house number' should be a non-empty string" in e for e in invalid_result['errors'])
    assert any("Field 'street' should be a non-empty string" in e for e in invalid_result['errors'])
    assert any("Field 'status' should be a boolean" in e for e in invalid_result['errors'])