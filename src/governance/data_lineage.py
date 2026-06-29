from datetime import datetime
import psycopg2
from src.config import settings

DDL = """
CREATE TABLE IF NOT EXISTS data_lineage (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMP DEFAULT NOW(),
    source TEXT,
    stage TEXT,
    destination TEXT,
    record_count INT
);
"""

PIPELINE_FLOW = ["YouTube", "Kafka", "Spark", "PostgreSQL"]


def _conn():
    return psycopg2.connect(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        dbname=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
    )


def init_table():
    with _conn() as c, c.cursor() as cur:
        cur.execute(DDL)
        c.commit()


def track(source, stage, destination, record_count=0):
    with _conn() as c, c.cursor() as cur:
        cur.execute(
            "INSERT INTO data_lineage (ts, source, stage, destination, record_count) "
            "VALUES (%s, %s, %s, %s, %s)",
            (datetime.utcnow(), source, stage, destination, record_count),
        )
        c.commit()


if __name__ == "__main__":
    init_table()
    track("YouTube CCTV", "ingestion->kafka", "traffic-events", 120)
    print("lineage:", " -> ".join(PIPELINE_FLOW))
