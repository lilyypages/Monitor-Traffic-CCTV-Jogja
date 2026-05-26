from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC = "traffic-events"


def send_traffic_data(data):
    producer.send(TOPIC, value=data)
    producer.flush()

    print(f"[KAFKA] Sent: {data}")