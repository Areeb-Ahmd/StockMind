import logging
import os
import sys
from datetime import datetime

# Create 'logs/' directory if it doesn't exist
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Create unique log file name
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

logger = logging.getLogger("stockmind")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s")

# File Handler
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setFormatter(formatter)
if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
    logger.addHandler(file_handler)

# Stdout Handler for Cloud Run / Container Logging
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
    logger.addHandler(stream_handler)