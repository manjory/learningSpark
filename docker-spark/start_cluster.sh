#!/bin/bash
echo "Starting Spark Docker cluster..."
docker-compose -f docker-compose.yml up -d
echo "Cluster started."
echo "Spark UI: http://localhost:8080"

chmod +x docker_spark/start_cluster.sh
