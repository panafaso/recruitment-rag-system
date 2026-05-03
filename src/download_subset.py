from datasets import load_dataset
import os

os.makedirs("data", exist_ok=True)

print("Loading dataset from Hugging Face...")
dataset = load_dataset("lang-uk/recruitment-dataset-candidate-profiles-english")

print("Available splits:", dataset)

print("Selecting first 20000 rows...")
subset = dataset["train"].select(range(20000))

print("Saving to local parquet...")
subset.to_parquet("data/candidate_profiles_20k.parquet")

print("Done!")
print("Saved file: data/candidate_profiles_20k.parquet")
print("Rows:", len(subset))
print("Columns:", subset.column_names)