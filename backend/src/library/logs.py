import logging
import os
from datetime import datetime

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def configure_logging():
    logs_directory = os.path.join("/app", "logs")
    os.makedirs(logs_directory, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    log_filename = os.path.join(logs_directory, f"{today}.txt")

    # Basic logging configuration
    logging.basicConfig(
        level=logging.INFO,  # Capture INFO and above
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )

    # Capture Uvicorn logs
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(logging.INFO)
    uvicorn_logger.addHandler(logging.FileHandler(log_filename))

    # Apply custom formatter to the console handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(CustomFormatter())
    logging.getLogger().addHandler(stream_handler)