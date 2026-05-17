import csv
import os
import logging
from datetime import datetime
from src.config.cameras import get_camera

LOG_DIR = "data/logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

error_logger = logging.getLogger("error")
error_handler = logging.FileHandler(f"{LOG_DIR}/error.log")
error_handler.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)
error_logger.setLevel(logging.ERROR)

def save_log(data, camera_id="malioboro_01"):
    filepath = f"{LOG_DIR}/traffic.csv"
    file_exists = os.path.isfile(filepath)
    fields = ["timestamp", "camera_id", "car", "motorcycle", "bus", "truck", "person", "total", "fps"]

    with open(filepath, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(fields)
        row = [data.get(f, 0) for f in fields]
        row[0] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow(row)

def get_logger():
    return logger

def get_error_logger():
    return error_logger
