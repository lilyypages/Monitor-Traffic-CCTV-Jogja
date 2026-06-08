#!/bin/bash

KAFKA_CONTAINER="traffic-kafka"

echo "Creating Kafka topics..."

docker exec $KAFKA_CONTAINER kafka-topics --create \
  --topic traffic-events \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

docker exec $KAFKA_CONTAINER kafka-topics --create \
  --topic traffic-alerts \
  --bootstrap-server localhost:9092 \
  --partitions 2 \
  --replication-factor 1 \
  --if-not-exists

docker exec $KAFKA_CONTAINER kafka-topics --create \
  --topic traffic-aggregated \
  --bootstrap-server localhost:9092 \
  --partitions 2 \
  --replication-factor 1 \
  --if-not-exists

echo ""
echo "Topics created:"
docker exec $KAFKA_CONTAINER kafka-topics --list --bootstrap-server localhost:9092
