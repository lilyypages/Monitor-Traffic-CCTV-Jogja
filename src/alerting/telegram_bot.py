import json
import requests
from kafka import KafkaConsumer
from src.config import settings


def send_telegram(message):
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        print("[telegram] token/chat_id belum diset, skip")
        return False
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    resp = requests.post(url, json=payload, timeout=10)
    return resp.ok


def format_alert(alert):
    return (
        "\U0001F6A8 <b>Traffic Alert</b>\n"
        f"Kamera: {alert.get('camera_id', '-')}\n"
        f"Kendaraan baru: {alert.get('delta', '-')}\n"
        f"Total: {alert.get('total', '-')}\n"
        f"Waktu: {alert.get('timestamp', '-')}"
    )


def run():
    consumer = KafkaConsumer(
        settings.TOPIC_ALERTS,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="latest",
        group_id="telegram-alerting",
    )
    print("[telegram] listening on", settings.TOPIC_ALERTS)
    for msg in consumer:
        alert = msg.value
        ok = send_telegram(format_alert(alert))
        print("[telegram] sent" if ok else "[telegram] failed", alert)


if __name__ == "__main__":
    run()
