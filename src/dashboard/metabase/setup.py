import requests
from src.config import settings

METABASE_URL = "http://metabase:3000"
MB_USER = "admin@traffic.local"
MB_PASS = "metabase123"


def get_session():
    resp = requests.post(
        f"{METABASE_URL}/api/session",
        json={"username": MB_USER, "password": MB_PASS},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["id"]


def add_postgres_database(session_id):
    headers = {"X-Metabase-Session": session_id}
    payload = {
        "engine": "postgres",
        "name": "Traffic DW",
        "details": {
            "host": settings.POSTGRES_HOST,
            "port": settings.POSTGRES_PORT,
            "dbname": settings.POSTGRES_DB,
            "user": settings.POSTGRES_USER,
            "password": settings.POSTGRES_PASSWORD,
            "ssl": False,
        },
    }
    resp = requests.post(
        f"{METABASE_URL}/api/database", json=payload, headers=headers, timeout=15
    )
    return resp.ok


if __name__ == "__main__":
    sid = get_session()
    print("postgres connected:", add_postgres_database(sid))
