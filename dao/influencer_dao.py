from dynamodb.connection import with_connection
from utils.logger_factory import get_logger
from utils.dao_utils import build_record,from_attributes_to_json
import constants.common as Common

logger = get_logger(__name__)

@with_connection
def create(dynamodb, influencer: dict):
    influencer = influencer | build_record()
    table = dynamodb.Table(Common.INFLUENCER)
    table.put_item(Item=influencer)
    logger.info("Created influencer successfully")
    return influencer

@with_connection
def find(dynamodb, influencer_id: str):
    table = dynamodb.Table(Common.INFLUENCER)
    response = table.get_item(Key={"id": influencer_id})
    if "Item" in response:
        return from_attributes_to_json(response["Item"])
    else:
        raise ValueError(f"User not found with ID: {influencer_id}")

@with_connection
def update(dynamodb, influencer: dict):
    table = dynamodb.Table(Common.INFLUENCER)
    influencer = influencer | build_record()
    update_fields = {k: v for k, v in influencer.items() if k != 'id'}
    update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in update_fields)
    expr_attr_values = {f":{k}": v for k, v in update_fields.items()}
    expr_attr_names = {f"#{k}": k for k in update_fields}

    response = table.update_item(
        Key={"id": influencer["id"]},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_attr_names,
        ExpressionAttributeValues=expr_attr_values,
        ReturnValues="ALL_NEW"
    )
    logger.info(f"Updated influencer with ID {influencer['id']} successfully")
    return response.get("Attributes", {})

@with_connection
def delete(dynamodb, influencer_id: str):
    if influencer_exists(influencer_id):
        table = dynamodb.Table(Common.INFLUENCER)
        table.delete_item(Key={"id": influencer_id})
        logger.info(f"Deleted {Common.INFLUENCER} successfully '{influencer_id}'")
        return {"action_type": f"{Common.INFLUENCER} deleted", "id": influencer_id}

@with_connection
def influencer_exists(dynamodb, influencer_id: str) -> bool:
    table = dynamodb.Table(Common.INFLUENCER)
    response = table.get_item(Key={"id": influencer_id})
    return "Item" in response

@with_connection
def find_all(dynamodb):
    table = dynamodb.Table(Common.INFLUENCER)
    response = table.scan()
    items = response.get("Items", [])
    if not items:
        logger.info(f"No influencer found in {Common.INFLUENCER}")
        return []
    logger.info(f"Fetched {len(items)} influencer from {Common.INFLUENCER}")
    return [from_attributes_to_json(item) for item in items]