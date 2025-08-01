# Docker-based Spark Cluster

## Overview

This project demonstrates running a Spark cluster using Docker containers with Bitnami Spark images. It covers:

- Starting a multi-node Spark cluster (master + workers)
- Submitting Spark jobs inside Docker containers
- Accessing Spark UI on the host machine
- Running example Spark jobs (word count, data join)
- Preparing for integration with Hive catalog tables, Delta Lake, and Apache Iceberg

---

## Prerequisites

- Docker installed and running  
- (Optional) `brew install pyspark` for local PySpark support  
- Basic command-line knowledge  

---

## How to Start the Cluster

```bash
cd docker_spark
./start_cluster.sh
```


## How to Stop the Cluster

    docker-compose down
    Access Spark UI
    Open your browser and go to:
    
    (arduino)
    http://localhost:8085
    (Port 8085 on the host maps to the Spark master UI port 8081 inside the container)
    
    Running Spark Jobs
    Get a shell inside the Spark master container:
    
    docker exec -it spark-master /bin/bash
    Submit a job inside the container:

spark-submit --master spark://spark-master:7077 --deploy-mode client /opt/bitnami/spark/imageWordCount.py
For new jobs (e.g., join on Hive catalog tables), add your PySpark scripts under /opt/bitnami/spark or mount a volume.

Python Virtual Environment Setup (Optional)
For local development with PySpark:

python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install pyspark
Run your PySpark scripts locally:

python pysparkTest.py
Dockerfile Snippet
Here is an example Dockerfile snippet that copies your PySpark scripts into the container:

## Dockerfile
FROM bitnami/spark:latest

USER root

COPY ./scripts/ /opt/bitnami/spark/

USER 1001
Place your Spark Python scripts inside the scripts/ folder locally.

Rebuild your Docker image after changes:

docker build -t testingwordcount:v1 .
docker-compose.yml Snippet

version: '3.8'

networks:
  spark-net:
    driver: bridge

services:
  spark-master:
    image: testingwordcount:v1
    container_name: spark-master
    hostname: spark-master
    ports:
      - "7077:7077"   # Spark master port
      - "8085:8081"   # Spark master UI port
    networks:
      - spark-net
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8085"]
      interval: 10s
      timeout: 5s
      retries: 5
    command: ["/opt/bitnami/scripts/spark/entrypoint.sh", "/opt/bitnami/scripts/spark/run.sh"]

  spark-worker-1:
    image: testingwordcount:v1
    container_name: spark-worker-1
    hostname: spark-worker-1
    depends_on:
      - spark-master
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
    networks:
      - spark-net

  spark-worker-2:
    image: testingwordcount:v1
    container_name: spark-worker-2
    hostname: spark-worker-2
    depends_on:
      - spark-master
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
    networks:
      - spark-net


## Notes on Logs and Troubleshooting
Spark logs show detailed INFO messages; focus on job stage submissions and completions.

Common WARN like NativeCodeLoader missing native Hadoop libs can be ignored.

If containers exit immediately after jobs, consider adding an entrypoint script or sleep command to keep them alive.

Use docker logs <container_name> to see logs.

Use lsof -i:<port> to check for port conflicts.

