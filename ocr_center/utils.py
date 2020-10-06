import logging
import os

LOG_LEVEL = logging.INFO
LOG_DIR = "log"
LOG_FILE = "ocr.log"


def get_logger(name, log_file=LOG_FILE, level=LOG_LEVEL):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logsh = logging.StreamHandler()
    logsh.setLevel(level)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    logsh.setFormatter(formatter)
    logger.addHandler(logsh)

    # file log
    if not os.path.isdir(LOG_DIR):
        os.mkdir(LOG_DIR)
    logfl = logging.FileHandler(os.path.join(LOG_DIR, log_file),
                                mode="w+", encoding="utf-8")
    logfl.setLevel(level)
    logfl.setFormatter(formatter)
    logger.addHandler(logfl)
    return logger


logger = get_logger(__name__)
