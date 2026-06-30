import os
import pandas as pd
import time

from src.kafka.producer import send_traffic_data

CSV_PATH = "data/logs/traffic.csv"

last_sent = None

def run_poller():
    global last_sent
    while True:
        if not os.path.isfile(CSV_PATH):
            time.sleep(5)
            continue

        df = pd.read_csv(CSV_PATH)
        if df.empty:
            time.sleep(5)
            continue

        latest = df.iloc[-1].to_dict()
        if latest == last_sent:
            time.sleep(5)
            continue

        send_traffic_data(latest)
        last_sent = latest
        print(f"[POLLER] Sent total={latest.get('total')} delta={latest.get('delta')}")

        time.sleep(5)

if __name__ == "__main__":
    run_poller()