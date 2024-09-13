import logging
import structlog

def get_logger():
    logging.basicConfig(level=logging.INFO)
    logger = structlog.get_logger()
    return logger