import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

DATA_PATH = "data/candidate_profiles_20k.parquet"
OUTPUT_EMBEDDINGS_PATH = "data/cv_embeddings_multilingual_e5_large.npy"

MODEL_NAME = "intfloat/multilingual-e5-large"
BATCH_SIZE = 32

device = "cuda" if torch.cuda.is_available() else "cpu"

print("=" * 80)
print(f"Using device: {device}")

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))

print("=" * 80)

df = pd.read_parquet(DATA_PATH)
print("Rows:", len(df))

print(f"Loading model: {MODEL_NAME}")

model = SentenceTransformer(
    MODEL_NAME,
    device=device
)

print("Model loaded!")
print("Model device:", model.device)

texts = [
    "passage: " + str(cv)
    for cv in df["CV"].fillna("")
]

print("Creating multilingual-e5-large CV embeddings...")

with torch.inference_mode():
    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=True
    )

print("Embeddings shape:", embeddings.shape)

np.save(
    OUTPUT_EMBEDDINGS_PATH,
    embeddings
)

print(f"Saved to: {OUTPUT_EMBEDDINGS_PATH}")