import pandas as pd
import time

from src.kafka.producer import send_traffic_data

CSV_PATH = "data/logs/traffic.csv"

def run_poller():
    while True:
        df = pd.read_csv(CSV_PATH)

        latest = df.iloc[-1].to_dict()

        send_traffic_data(latest)

        print("[POLLER] Sent latest row")

        time.sleep(5)

if __name__ == "__main__":
    run_poller()