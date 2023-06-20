# from .notifications import NotificationHandler
import time

from loguru import logger as _logger
from .settings import BASE_DIR


def config_logging():
    _logger.add(
        str(BASE_DIR) + "/logs/logs_{time}.log",
        level="DEBUG",
        format="{time} {level} {message}",
        rotation="5 MB",
        compression="zip"
    )


config_logging()

logger = _logger

if __name__ == '__main__':
    logger.info("Logger info")
    time.sleep(1)
    logger.error("Logger add error")
    time.sleep(1)
    logger.info("Logger add data")
