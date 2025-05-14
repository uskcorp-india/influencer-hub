from dynamodb.connection import with_connection
from utils.logger_factory import get_logger
from utils.dao_utils import build_record

QUESTION = 'question'
ANSWER = 'answer'
MESSAGE = "message"
ERROR="error"

logger = get_logger(__name__)

@with_connection
def create(dynamodb, customer: dict):
    customer = customer | build_record()
    table = dynamodb.Table("customer")
    table.put_item(Item=customer)
    logger.info("Created customer successfully")
    return customer
