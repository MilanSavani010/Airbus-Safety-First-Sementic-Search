import logging
from config import LOG_LEVEL

def get_logger(name="pdf_indexer"):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))

    if not logger.hasHandlers():
        formatter = logging.Formatter("[%(levelname)s] %(asctime)s :: %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger