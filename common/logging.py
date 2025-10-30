import logging
import json
import uuid

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def log_event(logger: logging.Logger, event: str, **kwargs):
    payload = {"event": event, "correlation_id": str(uuid.uuid4()), **kwargs}
    logger.info(json.dumps(payload))
