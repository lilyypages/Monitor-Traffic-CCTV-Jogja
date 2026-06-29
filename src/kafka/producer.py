import json
from kafka import KafkaProducer
from src.config import settings

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

TOPIC = settings.TOPIC_EVENTS


def send_traffic_data(data):
    producer.send(TOPIC, value=data)
    producer.flush()
    print(f"[KAFKA] Sent: {data}")