#!/bin/bash
set -e

export PYTHONPATH=/opt/spark-app
export SPARK_MASTER=local[2]
export KAFKA_BROKER=kafka:29092
export DB_HOST=postgres
export DB_PORT=5432
export DB_NAME=traffic_db
export DB_USER=postgres
export DB_PASSWORD=postgres

PACKAGES="org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.postgresql:postgresql:42.7.3"

echo "[spark-init] Pre-downloading Maven packages..."
/opt/spark/bin/spark-submit \
  --master "$SPARK_MASTER" \
  --packages "$PACKAGES" \
  /opt/spark-app/src/spark/streaming/dummy_job.py \
  > /tmp/logs/predownload.log 2>&1
echo "[spark-init] Packages cached."

sleep 2

echo "[spark-init] Starting density query..."
/opt/spark/bin/spark-submit \
  --master "$SPARK_MASTER" \
  --packages "$PACKAGES" \
  /opt/spark-app/src/spark/streaming/density_query.py \
  > /tmp/logs/density.log 2>&1 &
echo "[spark-init] density_query PID=$!"

sleep 3

echo "[spark-init] Starting traffic count query..."
/opt/spark/bin/spark-submit \
  --master "$SPARK_MASTER" \
  --packages "$PACKAGES" \
  /opt/spark-app/src/spark/streaming/traffic_count_query.py \
  > /tmp/logs/count.log 2>&1 &
echo "[spark-init] traffic_count_query PID=$!"

sleep 3

echo "[spark-init] Starting aggregation query..."
/opt/spark/bin/spark-submit \
  --master "$SPARK_MASTER" \
  --packages "$PACKAGES" \
  /opt/spark-app/src/spark/streaming/aggregation_query.py \
  > /tmp/logs/aggregation.log 2>&1 &
echo "[spark-init] aggregation_query PID=$!"

echo "[spark-init] All Spark streaming jobs started. Waiting..."
wait
