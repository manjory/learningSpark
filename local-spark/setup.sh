#Local Standalone Spark

### `local_spark/setup.sh`

```bash
#!/bin/bash

# Download Spark if not already downloaded
if [ ! -d "spark-3.5.0-bin-hadoop3" ]; then
  echo "Downloading Spark..."
  wget https://downloads.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
  tar -xzf spark-3.5.0-bin-hadoop3.tgz
fi

export SPARK_HOME=$(pwd)/spark-3.5.0-bin-hadoop3
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

echo "Spark setup complete."
echo "Run the following to start master and workers:"
echo "  $SPARK_HOME/sbin/start-master.sh"
echo "  $SPARK_HOME/sbin/start-worker.sh spark://localhost:7077"
