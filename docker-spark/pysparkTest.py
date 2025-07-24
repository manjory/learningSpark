from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ManjoryTestCluster").master("spark://localhost:7077").config("spark.executor.memory","1g").config("spark.executor.cores","1").getOrCreate()

print("Spark Version::",spark.version)

df = spark.createDataFrame([(1, "apple"), (2, "banana"), (3, "cherry")], ["id", "fruit"])
df.show()

spark.stop()

