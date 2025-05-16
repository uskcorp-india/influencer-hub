import dynamodb.dynamodb_proxy as db
from utils.logger_factory import get_logger
import validator.influencer_validator as validator
from utils.response_utils import build_response

logger = get_logger(__name__)

def create(influencer: dict):
    validated_influencer = validator.validate(influencer)
    logger.info(f'influencer details: {influencer}')

    if 'errors' in validated_influencer:
        return build_response(validated_influencer['errors'],400)
    else:
        response = db.create_influencer(influencer)
        return build_response(response,'influencer Created Successfully')

def find(influencer_id: str):
    response = db.find_influencer(influencer_id)
    logger.info(response)
    return build_response(response,"influencer Found Successfully")

def update(influencer: dict):
    validated_influencer = validator.validate(influencer)
    logger.info(f'Updating customer details: {influencer}')

    if 'errors' in validated_influencer:
        return build_response(validated_influencer['errors'], 400)
    else:
        response = db.update_influencer(influencer)
        return build_response(response, 'influencer Updated Successfully')

def delete(influencer_id:str):
    response=db.delete_influencer(influencer_id)
    logger.info(response)
    return build_response(response,message="influencer deleted successfully")

def find_all():
    response = db.find_all_influencer()
    logger.info(f"Total influencer fetched: {len(response)}")
    return build_response(response, "All influencer Fetched Successfully")