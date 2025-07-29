import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, concat_ws
import requests
import os

def download_dataset(url, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    filename = url.split("/")[-1]
    file_path = os.path.join(dst_dir, filename)

    if not os.path.exists(file_path):
        print(f"Downloading to: {file_path}")
        r = requests.get(url)
        with open(file_path, "wb") as f:
            f.write(r.content)
    else:
        print(f"File already exists at: {file_path}")

    return file_path

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
    dst_dir = "./dst"
    csv_file_path = download_dataset(url, dst_dir)

    # Step 2: Spark Session
    spark = SparkSession.builder.appName("GHG-DataLoader").getOrCreate()

    # Step 3: Read CSV
    df = spark.read.option("header", True).csv(csv_file_path)
    df.printSchema()

    # Step 4: Word Count Before Merge
    print("🔁 Word Count BEFORE merge:")
    run_word_count(df)

    # Step 5: Merge GHG + Unit (stubbed for now)
    df = merge_ghg_unit_columns(df)

    # Step 6: Word Count After Merge
    print("🔁 Word Count AFTER merge:")
    run_word_count(df)

    # Step 7: View Sample Output
    df.show(10, truncate=False)

    # Step 8: Save to JSON (you could also do .json())
    df.write.mode("overwrite").csv(dst_dir + "/output")
    time.sleep(5)
    spark.stop()
    print("✅ Spark job completed.")
if __name__ == "__main__":
    main()
