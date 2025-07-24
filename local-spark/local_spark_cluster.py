from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("LocalSparkTest")\
    .master("local[4]")\
    .config("spark.executor.memory", "1g")\
    .config("spark.executor.cores", "1")\
    .config("spark.executor.instances", "3")\
    .getOrCreate() # 1 driver + 3 executors simulated by threads \

data = [(i, f"item_{i}") for i in range(10)]
df = spark.createDataFrame(data, ["id", "name"])
df.show()

spark.stop()

