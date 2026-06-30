import json
from kafka import KafkaConsumer, KafkaProducer
from src.config import settings


THRESHOLD = settings.DENSITY_THRESHOLD

consumer = KafkaConsumer(
    settings.TOPIC_EVENTS,
    bootstrap_servers=settings.KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="latest",
    group_id="alert-processor",
)

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def run():
    print(f"[alert-processor] listening on {settings.TOPIC_EVENTS}, threshold={THRESHOLD}")
    for msg in consumer:
        data = msg.value
        vehicles_now = (
            data.get("car", 0)
            + data.get("motorcycle", 0)
            + data.get("bus", 0)
            + data.get("truck", 0)
        )
        if vehicles_now > THRESHOLD:
            alert = {
                "timestamp": data.get("timestamp", ""),
                "camera_id": data.get("camera_id", ""),
                "vehicles": vehicles_now,
                "total": data.get("total", 0),
            }
            producer.send(settings.TOPIC_ALERTS, value=alert)
            producer.flush()
            print(f"[alert-processor] ALERT sent: {alert}")
        else:
            print(f"[alert-processor] vehicles={vehicles_now} <= {THRESHOLD}, no alert")


if __name__ == "__main__":
    run()
