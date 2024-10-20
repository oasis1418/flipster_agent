import logging
import logging.config
import os
from datetime import datetime
import sys
from settings.argument_config import get_argument

now_date = datetime.now().strftime("%Y-%m-%d %H:%M")
device_name = get_argument("device_name")


def log_dir():
    if os.path.exists("./logs") == False:
        os.makedirs("./logs")
    return "./logs/"


config = {
    "version": 1,
    "formatters": {
        "basic": {"format": "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] - %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "basic",
            "level": "INFO",
            "stream": "ext://sys.stdout",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": f"{log_dir()}{device_name}_{now_date}.log",
            "formatter": "basic",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console", "file_handler"],
        "level": "INFO",
    },
}

logging.config.dictConfig(config)

logger = logging.getLogger()
