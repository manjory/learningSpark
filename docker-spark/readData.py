import pandas as pd

csv_file_path="/Users/macbookpro_2015/dev/SupplyChainGreenhouseGasEmissionFactors.csv"


try:
    df = pd.read_csv(csv_file_path)
    print(df.head())

except FileNotFoundError:
    print("SupplyChainGreenhouseGasEmissionFactors file not found")

except Exception as e:
    print("error occurred",e)
