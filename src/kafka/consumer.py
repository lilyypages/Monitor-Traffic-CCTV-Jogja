import json
from kafka import KafkaConsumer
from src.config import settings

consumer = KafkaConsumer(
    settings.TOPIC_EVENTS,
    bootstrap_servers=settings.KAFKA_BROKER,
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

print("Listening Kafka topic...")

for message in consumer:
    data = message.value
    print(
        f"\nTimestamp : {data['timestamp']}"
        f"\nCamera    : {data['camera_id']}"
        f"\nTotal     : {data['total']}"
        f"\nFPS       : {data.get('fps')}"
    )