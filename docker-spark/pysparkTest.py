from pyspark.sql import SparkSession

# spark = SparkSession.builder.appName("ManjoryTestCluster").master("spark://localhost:7077").config("spark.executor.memory","1g").config("spark.executor.cores","1").getOrCreate()
#
# print("Spark Version::",spark.version)
#
# df = spark.createDataFrame([(1, "apple"), (2, "banana"), (3, "cherry")], ["id", "fruit"])
# df.show()
#
# spark.stop()


if __name__=="__main__":
    spark=SparkSession.builder.appName("WordCount").getOrCreate()
    sc=spark.sparkContext

    lines=sc.textFile("/Users/macbookpro_2015/dev/python/learningSpark/docker-spark/hello-world.txt")

    counts=(
        lines.flatMap(lambda line: line.split())
    .map(lambda word: (word,1))
    .reduceByKey(lambda a,b: a+b)
    )
    counts.saveAsTextFile("/Users/macbookpro_2015/dev/python/learningSpark/docker-spark/opt/spark-data/output.txt")
    spark.stop()
