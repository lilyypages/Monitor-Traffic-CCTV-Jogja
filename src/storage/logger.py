import csv
import os
import psycopg2
from datetime import datetime
from src.utils.helpers import get_logger

import os

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "traffic_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432))
}

CSV_DIR = "data/logs"
os.makedirs(CSV_DIR, exist_ok=True)

logger = get_logger()

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.warning(f"PostgreSQL tidak tersedia: {e}")
        return None

def create_table():
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS traffic_logs (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP,
                camera_id TEXT,
                car INT,
                motorcycle INT,
                bus INT,
                truck INT,
                person INT,
                total INT,
                fps FLOAT
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Tabel traffic_logs siap di PostgreSQL")
    except Exception as e:
        logger.error(f"Gagal buat tabel: {e}")

def save_to_postgres(data):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO traffic_logs (timestamp, camera_id, car, motorcycle, bus, truck, person, total, fps)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            datetime.now(), data.get("camera_id"),
            data.get("car", 0), data.get("motorcycle", 0),
            data.get("bus", 0), data.get("truck", 0),
            data.get("person", 0), data.get("total", 0), data.get("fps", 0.0)
        ))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Gagal simpan ke PostgreSQL: {e}")
        return False

def save_to_csv(data):
    filepath = f"{CSV_DIR}/traffic.csv"
    file_exists = os.path.isfile(filepath)
    fields = ["timestamp", "camera_id", "car", "motorcycle", "bus", "truck", "person", "total", "fps"]
    with open(filepath, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(fields)
        row = [data.get(f, 0) for f in fields]
        row[0] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow(row)

def save_data(data):
    save_to_csv(data)
    ok = save_to_postgres(data)
    if ok:
        logger.info(f"Data tersimpan ke PostgreSQL & CSV: total={data.get('total')}")
    else:
        logger.info(f"Data tersimpan ke CSV (fallback): total={data.get('total')}")
