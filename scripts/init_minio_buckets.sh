#!/bin/bash

export MC_HOST_local=http://minioadmin:minioadmin@localhost:9000

echo "Creating MinIO buckets..."

mc mb local/traffic-raw --ignore-existing
mc mb local/traffic-processed --ignore-existing
mc mb local/traffic-ml-results --ignore-existing

echo ""
echo "Buckets:"
mc ls local
