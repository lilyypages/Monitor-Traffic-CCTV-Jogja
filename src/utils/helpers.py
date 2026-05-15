import csv
import os
from datetime import datetime

FILE_PATH = "data/logs/traffic.csv"

def save_log(location, count):

    file_exists = os.path.isfile(FILE_PATH)

    with open(FILE_PATH, mode="a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "location",
                "vehicle_count"
            ])

        writer.writerow([
            datetime.now(),
            location,
            count
        ])