from validator.influencer_validator import validate

def test_validate_with_valid_influencer():
    influencer = {
        'name': 'Alice',
        'email': 'alice123@example.com',
        'phone': '9876543210',
        'platform': 'Instagram',
        'followers': 15000,
        'id': 'inf123',
        'username': 'alice_insta',
        'bio': 'Fashion enthusiast',
        'category': 'fashion',
        'location': 'NYC',
        'language': 'English',
        'age': 25,
        'gender': 'female',
        'engagement_rate': 75,
        'collaboration_interest': True,
        'content_types': 'photos, videos',
        'status': True,
        'created_at': '2024-01-01',
        'updated_at': '2024-02-01',
    }

    result = validate(influencer)
    assert 'errors' not in result
    assert result['name'] == influencer['name']
    assert result['email'] == influencer['email']
    assert result['phone'] == influencer['phone']
    assert result['platform'] == influencer['platform']
    assert result['followers'] == influencer['followers']
    assert result['id'] == influencer['id']
    assert result['username'] == influencer['username']
    assert result['bio'] == influencer['bio']
    assert result['category'] == influencer['category']
    assert result['location'] == influencer['location']
    assert result['language'] == influencer['language']
    assert result['age'] == influencer['age']
    assert result['gender'] == influencer['gender']
    assert result['engagement_rate'] == influencer['engagement_rate']
    assert result['collaboration_interest'] == influencer['collaboration_interest']
    assert result['content_types'] == influencer['content_types']
    assert result['status'] == influencer['status']
    assert result['created_at'] == influencer['created_at']
    assert result['updated_at'] == influencer['updated_at']

def test_validate_with_invalid_values():
    influencer = {
        'name': '',
        'email': 'wrongemail@domain',
        'phone': '1234abc678',
        'platform': '',
        'followers': -1,
        'age': 10,
        'gender': 'unknown',
        'engagement_rate': 150,
        'collaboration_interest': 'yes',
        'status': 'active',
    }
    result = validate(influencer)
    assert 'errors' in result

    expected_errors = [
        "Field 'name' should be a non-empty string",
        "Invalid email format",
        "Phone number must be a 10-digit number",
        "Field 'platform' should be a non-empty string",
        "Field 'followers' should be a non-negative integer",
        "Age must be between 13 and 100",
        "Gender must be 'male', 'female', or 'other'",
        "Engagement rate must be an integer between 0 and 100",
        "Field 'collaboration_interest' should be a boolean",
        "Field 'status' should be a boolean",
    ]

    for expected_error in expected_errors:
        assert any(expected_error in error for error in result['errors']), f"Expected error '{expected_error}' not found"

def test_validate_with_missing_required_fields():
    influencer = {
        'email': 'invalid-email',
        'followers': -10,
    }
    result = validate(influencer)
    assert 'errors' in result

    expected_errors = [
        "Missing required field: name",
        "Missing required field: phone",
        "Missing required field: platform",
        "Invalid email format",
        "Field 'followers' should be a non-negative integer",
    ]
    for expected_error in expected_errors:
        assert any(expected_error in error for error in result['errors']), f"Expected error '{expected_error}' not found"

def test_validate_with_invalid_phone():
    influencer = {
        'name': 'Bob',
        'email': 'bob@example.com',
        'phone': '12345abcde',
        'platform': 'YouTube',
        'followers': 1000,
    }
    result = validate(influencer)
    assert 'errors' in result
    assert "Phone number must be a 10-digit number" in result['errors']

def test_validate_with_missing_optional_fields():
    influencer = {
        'name': 'Eva Green',
        'email': 'eva.green@example.com',
        'phone': '9876543210',
        'platform': 'Instagram',
        'followers': 8000
    }
    result = validate(influencer)
    assert 'errors' not in result
    assert result['name'] == influencer['name']
    assert result['email'] == influencer['email']
    assert result['phone'] == influencer['phone']
    assert result['platform'] == influencer['platform']
    assert result['followers'] == influencer['followers']

def test_invalidate_with_missing_optional_fields():
    influencer = {
        'name': 'Alice Smith',
        'email': 'alice.smith@example.com',
        'phone': '1234567890',
        'platform': 'Instagram',
        'followers': 5000,
        'age': 120,
        'gender': 'robot'
    }

    result = validate(influencer)

    assert 'errors' in result
    assert "Age must be between 13 and 100" in result['errors']
    assert "Gender must be 'male', 'female', or 'other'" in result['errors']
