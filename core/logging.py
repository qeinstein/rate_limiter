import logging
import json
from typing import Any, Dict

def get_logger():
    logger = logging.getLogger("day1_service")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def log_event(logger, event: Dict[str, Any]):
    #convert to JSON one liner
    logger.info(json.dumps(event, default=str))

