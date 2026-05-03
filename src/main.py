import pandas as pd

df = pd.read_parquet("data/candidate_profiles_20k.parquet")

print("Rows:", len(df))
print(df.columns.tolist())
print(df["CV"].iloc[0][:1500])