import logging
import sys
from pathlib import Path

LOG_FILE = Path("logs/rfid_server.log")
LOG_FILE.parent.mkdir(exist_ok=True)

logger = logging.getLogger("rfid_server_api")


def initialize_logger():
    if LOG_FILE.exists():
        LOG_FILE.unlink()

    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


initialize_logger()
