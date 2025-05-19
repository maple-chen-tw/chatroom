import logging
import os

APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = logging.DEBUG if APP_ENV == "development" else logging.INFO

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

def get_logger(name=None):
    return logging.getLogger(name or "chatroom")
