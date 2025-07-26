from pyspark.sql import SparkSession

import requests
import os

url = "https://pasteur.epa.gov/uploads/10.23719/1531143/SupplyChainGHGEmissionFactors_v1.3.0_NAICS_CO2e_USD2022.csv"
local_path = "/tmp/SupplyChainGHGEmissionFactors.csv"
if not os.path.exists(local_path):
    print("Downloading dataset...")
    response = requests.get(url)
    with open(local_path, "wb") as f:
        f.write(response.content)
    print("Download complete.")
else:
    print("File already downloaded.")





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
