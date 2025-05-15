import dynamodb.dynamodb_proxy as db
from utils.logger_factory import get_logger
import validator.customer_validator as validator
from utils.response_utils import build_response

logger = get_logger(__name__)

def create(customer: dict):
    validated_customer = validator.validate(customer)
    logger.info(f'customer details: {customer}')

    if 'errors' in validated_customer:
        return build_response(validated_customer['errors'],400)
    else:
        response = db.create_customer(customer)
        return build_response(response,'customer Created Successfully')

def update(customer: dict):
    validated_customer = validator.validate(customer)
    logger.info(f'Updating customer details: {customer}')

    if 'errors' in validated_customer:
        return build_response(validated_customer['errors'], 400)
    else:
        response = db.update_customer(customer)
        return build_response(response, 'Customer Updated Successfully')