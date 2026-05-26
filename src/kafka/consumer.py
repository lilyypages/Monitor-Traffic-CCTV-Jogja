from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "traffic-events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Listening Kafka topic...")

for message in consumer:
    data = message.value

    print(f"""
Timestamp : {data['timestamp']}
Camera    : {data['camera_id']}
Total     : {data['total']}
FPS       : {data['fps']}
""")