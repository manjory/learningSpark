from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, concat_ws
import requests
import os

def download_dataset(url: str, local_path: str):
    """Download file if it doesn't exist locally."""
    if not os.path.exists(local_path):
        print("⬇️ Downloading dataset...")
        response = requests.get(url)
        with open(local_path, "wb") as f:
            f.write(response.content)
        print("✅ Download complete.")
    else:
        print("📂 File already exists locally.")

def run_word_count(df):
    """Run a basic word count on the first text column found."""
    text_col = None
    for col_name in df.columns:
        if df.schema[col_name].dataType.simpleString() == "string":
            text_col = col_name
            break

    if not text_col:
        print("⚠️ No string column found for word count.")
        return

    print(f"🔤 Running word count on column: {text_col}")
    words = df.select(explode(split(col(text_col), "\\s+")).alias("word"))
    word_counts = words.groupBy("word").count().orderBy("count", ascending=False)
    word_counts.show(10, truncate=False)

def merge_ghg_unit_columns(df):
    """Merge GHG and Unit into 'GHG and Units'."""
    cols = df.columns
    print("📋 Available columns:", cols)
    if "GHG" in cols and "Unit" in cols:
        df.select("GHG", "Unit").show(5, truncate=False)
        print("✅ Merging 'GHG' and 'Unit' columns...")
        df = df.withColumn("GHG and Units", concat_ws(", ", col("GHG"), col("Unit")))
        df = df.drop("GHG").drop("Unit")
    else:
        print("⚠️ Columns 'GHG' and/or 'Unit' not found. Skipping merge.")
    return df

def main():
    # Step 1: Download
    url = "https://pasteur.epa.gov/uploads/10.23719/1531143/SupplyChainGHGEmissionFactors_v1.3.0_NAICS_CO2e_USD2022.csv"
    local_path = "/tmp/SupplyChainGHGEmissionFactors.csv"
    download_dataset(url, local_path)

    # Step 2: Spark Session
    spark = SparkSession.builder.appName("GHG-DataLoader").getOrCreate()

    # Step 3: Read CSV
    df = spark.read.option("header", True).csv(local_path)
    df.printSchema()

    # Step 4: Word Count Before Merge
    print("🔁 Word Count BEFORE merge:")
    run_word_count(df)

    # Step 5: Merge GHG + Unit
    df = merge_ghg_unit_columns(df)

    # Step 6: Word Count After Merge
    print("🔁 Word Count AFTER merge:")
    run_word_count(df)

    # Step 7: View Sample Output
    df.show(10, truncate=False)

    # Step 8: Save to JSON
    df.write.mode("overwrite").json("/tmp/spark-ghg-output.json")

    spark.stop()
    print("✅ Spark job completed.")

if __name__ == "__main__":
    main()
