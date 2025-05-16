from dynamodb.connection import with_connection
from utils.logger_factory import get_logger
from utils.dao_utils import build_record
import constants.common as Common
from utils.dao_utils import from_attributes_to_json


logger = get_logger(__name__)

@with_connection
def create(dynamodb, customer: dict):
    customer = customer | build_record()
    table = dynamodb.Table(Common.CUSTOMER)
    table.put_item(Item=customer)
    logger.info("Created customer successfully")
    return customer

@with_connection
def find(dynamodb, customer_id: str):
    table = dynamodb.Table(Common.CUSTOMER)
    response = table.get_item(Key={"id": customer_id})
    if "Item" in response:
        return from_attributes_to_json(response["Item"])
    else:
        raise ValueError(f"User not found with ID: {customer_id}")

@with_connection
def update(dynamodb, customer: dict):
    table = dynamodb.Table(Common.CUSTOMER)
    customer = customer | build_record()
    update_fields = {k: v for k, v in customer.items() if k != 'id'}
    update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in update_fields)
    expr_attr_values = {f":{k}": v for k, v in update_fields.items()}
    expr_attr_names = {f"#{k}": k for k in update_fields}

    response = table.update_item(
        Key={"id": customer["id"]},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_attr_names,
        ExpressionAttributeValues=expr_attr_values,
        ReturnValues="ALL_NEW"
    )
    logger.info(f"Updated customer with ID {customer['id']} successfully")
    return response.get("Attributes", {})

@with_connection
def delete(dynamodb, customer_id: str):
    if customer_exists(customer_id):
        table = dynamodb.Table(Common.CUSTOMER)
        table.delete_item(Key={"id": customer_id})
        logger.info(f"Deleted {Common.CUSTOMER} successfully '{customer_id}'")
        return {"action_type": f"{Common.CUSTOMER} deleted", "id": customer_id}

@with_connection
def customer_exists(dynamodb, customer_id: str) -> bool:
    table = dynamodb.Table(Common.CUSTOMER)
    response = table.get_item(Key={"id": customer_id})
    return "Item" in response

@with_connection
def find_all(dynamodb):
    table = dynamodb.Table(Common.CUSTOMER)
    response = table.scan()
    items = response.get("Items", [])
    if not items:
        logger.info(f"No customers found in {Common.CUSTOMER}")
        return []
    logger.info(f"Fetched {len(items)} customers from {Common.CUSTOMER}")
    return [from_attributes_to_json(item) for item in items]