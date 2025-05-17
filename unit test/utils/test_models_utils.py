import utils.models as models

def test_model_enum_values():
    assert models.Model.INFLUENCER.value == "INFLUENCER"
    assert models.Model.CUSTOMER.value == "CUSTOMER"

def test_model_enum_membership():
    assert "INFLUENCER" in models.Model.__members__
    assert "CUSTOMER" in models.Model.__members__

def test_operation_enum_values():
    assert models.Operation.CREATE.value == "CREATE"
    assert models.Operation.UPDATE.value == "UPDATE"
    assert models.Operation.DELETE.value == "DELETE"

def test_operation_enum_membership():
    assert "CREATE" in models.Operation.__members__
    assert "UPDATE" in models.Operation.__members__
    assert "DELETE" in models.Operation.__members__

def test_enum_instance_types():
    assert isinstance(models.Model.INFLUENCER, models.Model)
    assert isinstance(models.Model.CUSTOMER, models.Model)
    assert isinstance(models.Operation.CREATE, models.Operation)