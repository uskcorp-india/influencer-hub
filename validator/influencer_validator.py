import re
from schema import Schema, And, Optional, SchemaError

def validate(influencer: dict) -> dict:
    errors = []
    field_validators = {
        'name': And(str, len, error="Field 'name' should be a non-empty string"),
        'email': And(str, lambda s: bool(re.match(
            r'^[a-zA-Z][a-zA-Z0-9._]*@[a-zA-Z0-9-]+\.(?:com|in|co\.in)$', s)),
            error="Invalid email format"),
        'phone': And(str, lambda s: len(s) == 10 and s.isdigit(), error="Phone number must be a 10-digit number"),
        'platform': And(str, len, error="Field 'platform' should be a non-empty string"),
        'followers': And(int, lambda n: n >= 0, error="Field 'followers' should be a non-negative integer"),

        Optional('id'): And(str, len, error="Field 'id' should be a non-empty string"),
        Optional('username'): And(str, len, error="Field 'username' should be a non-empty string"),
        Optional('bio'): And(str, len, error="Field 'bio' should be a non-empty string"),
        Optional('category'): And(str, len, error="Field 'category' should be a non-empty string"),  # e.g., fashion, tech
        Optional('location'): And(str, len, error="Field 'location' should be a non-empty string"),
        Optional('language'): And(str, len, error="Field 'language' should be a non-empty string"),
        Optional('age'): And(int, lambda n: 13 <= n <= 100, error="Age must be between 13 and 100"),
        Optional('gender'): And(str, lambda g: g.lower() in ['male', 'female', 'other'], error="Gender must be 'male', 'female', or 'other'"),
        Optional('engagement_rate'): And(int,lambda x: 0 <= x <= 100,error="Engagement rate must be an integer between 0 and 100" ),
        Optional('collaboration_interest'): And(bool, error="Field 'collaboration_interest' should be a boolean"),
        Optional('content_types'): And(str, error="Field 'content_types' should be a string"),
        Optional('status'): And(bool, error="Field 'status' should be a boolean"),
        Optional('created_at'): And(str, len, error="Field 'created_at' should be a non-empty string"),
        Optional('updated_at'): And(str, len, error="Field 'updated_at' should be a non-empty string"),
    }

    validated_influencer = {}
    for key, validator in field_validators.items():
        key_name = key.schema if isinstance(key, Optional) else key

        if key_name in influencer:
            try:
                validated_influencer[key_name] = Schema(validator).validate(influencer[key_name])
            except SchemaError as e:
                errors.append(str(e))
        else:
            if not isinstance(key, Optional):
                errors.append(f"Missing required field: {key_name}")

    if errors:
        return {"errors": errors}
    return validated_influencer