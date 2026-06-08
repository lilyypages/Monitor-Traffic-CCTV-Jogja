#!/bin/bash

echo "=== Traffic Monitor Setup ==="

echo ""
echo "1. Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "2. Creating data directories..."
mkdir -p data/logs models

echo ""
echo "3. Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "  -> .env created from .env.example"
fi

echo ""
echo "4. Starting Docker containers..."
docker-compose down
docker-compose up -d

echo ""
echo "5. Initializing Kafka topics..."
sleep 10
bash scripts/init_kafka_topics.sh

echo ""
echo "6. Initializing MinIO buckets..."
sleep 5
bash scripts/init_minio_buckets.sh

echo ""
echo "=== SETUP DONE ==="
echo "Grafana  : http://localhost:3000 (admin/admin)"
echo "Metabase : http://localhost:3001"
echo "Spark    : http://localhost:8080"
echo "MinIO    : http://localhost:9001 (minioadmin/minioadmin)"
