from datetime import datetime
import psycopg2
from src.config import settings

DDL = """
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMP DEFAULT NOW(),
    user_role TEXT,
    action TEXT,
    resource TEXT,
    detail TEXT
);
"""


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


def log_action(user_role, action, resource, detail=""):
    with _conn() as c, c.cursor() as cur:
        cur.execute(
            "INSERT INTO audit_logs (ts, user_role, action, resource, detail) "
            "VALUES (%s, %s, %s, %s, %s)",
            (datetime.utcnow(), user_role, action, resource, detail),
        )
        c.commit()


if __name__ == "__main__":
    init_table()
    log_action("analyst", "view_dashboard", "grafana", "buka panel density")
    print("audit log recorded")
