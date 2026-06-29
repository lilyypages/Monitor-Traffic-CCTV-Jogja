import os

# Kafka — docker-compose ngasih env KAFKA_BROKER=kafka:29092 (listener internal antar-container); dari host pakai localhost:9092
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_BOOTSTRAP_SERVERS = KAFKA_BROKER  # alias biar konsisten sama kode lain
TOPIC_EVENTS = os.getenv("TOPIC_EVENTS", "traffic-events")
TOPIC_ALERTS = os.getenv("TOPIC_ALERTS", "traffic-alerts")
TOPIC_AGGREGATED = os.getenv("TOPIC_AGGREGATED", "traffic-aggregated")

# Threshold & interval
DENSITY_THRESHOLD = int(os.getenv("DENSITY_THRESHOLD", "100"))
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "5"))

# PostgreSQL — disamain sama src/storage/logger.py: pakai env DB_* dan dbname "traffic_db"
POSTGRES_HOST = os.getenv("DB_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("DB_PORT", "5432"))
POSTGRES_DB = os.getenv("DB_NAME", "traffic_db")
POSTGRES_USER = os.getenv("DB_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# MinIO
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() == "true"

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# SMTP / Email
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO", "")


def postgres_uri():
    return (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
