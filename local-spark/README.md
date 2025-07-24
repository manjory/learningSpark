# Local Standalone Spark Setup

## Setup Spark locally

```bash
cd local_spark
./setup.sh
```
### Start Spark master and workers


$SPARK_HOME/sbin/start-master.sh
$SPARK_HOME/sbin/start-worker.sh spark://localhost:7077
$SPARK_HOME/sbin/start-worker.sh spark://localhost:7077
$SPARK_HOME/sbin/start-worker.sh spark://localhost:7077

### Run PySpark script
python3 local_spark_script.py


## Access Spark UI

open : http://localhost:8080


---

## Root README.md (overview)

# Spark Learning Project

This project contains two Spark environment setups:

1. **Docker-based Spark Cluster** (`docker_spark/`):  
   A Spark master + 3 worker nodes running inside Docker containers.

2. **Local Standalone Spark** (`local_spark/`):  
   Spark installed and run manually on your local machine.

---

## How to use

- To use Docker Spark cluster, go to `docker_spark/` and follow instructions in its README.md  
- To use Local Spark setup, go to `local_spark/` and follow instructions in its README.md

---

Happy learning! 🚀
