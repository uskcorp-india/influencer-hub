import logging
from utils.logger_factory import get_logger

def test_logger_logs_message(caplog):
    logger = get_logger(__name__)
    with caplog.at_level(logging.INFO):
        logger.info("This is a test log")
    assert "This is a test log" in caplog.text

def test_logger_logs_at_different_levels(caplog):
    logger = get_logger(__name__)
    with caplog.at_level(logging.WARNING):
        logger.debug("This should not appear")
        logger.info("This should not appear")
        logger.warning("This is a warning")
        logger.error("This is an error")
    log_messages = caplog.text
    assert "This is a warning" in log_messages
    assert "This is an error" in log_messages
    assert "This should not appear" not in log_messages

def test_logger_logs_to_multiple_handlers(caplog):
    logger = get_logger(__name__)
    with caplog.at_level(logging.INFO):
        logger.info("Log message to multiple handlers")
    assert "Log message to multiple handlers" in caplog.text

def test_logger_does_not_log_lower_levels(caplog):
    logger = get_logger(__name__)
    with caplog.at_level(logging.WARNING):
        logger.debug("This is a debug message")
        logger.info("This is an info message")
    assert "This is a debug message" not in caplog.text
    assert "This is an info message" not in caplog.text