import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

DATA_PATH = "data/candidate_profiles_20k.parquet"
OUTPUT_EMBEDDINGS_PATH = "data/cv_embeddings_bge_m3.npy"

MODEL_NAME = "BAAI/bge-m3"
BATCH_SIZE = 32

device = "cuda" if torch.cuda.is_available() else "cpu"

print("=" * 80)
print(f"Using device: {device}")

if torch.cuda.is_available():
    print("CUDA available:", torch.cuda.is_available())
    print("GPU:", torch.cuda.get_device_name(0))
    print("CUDA version:", torch.version.cuda)

print("=" * 80)

df = pd.read_parquet(DATA_PATH)
print("Rows:", len(df))


def safe_value(x):
    return "" if pd.isna(x) else str(x)


def build_cv_text(row):
    parts = [
        safe_value(row.get("Position")),
        safe_value(row.get("Primary Keyword")),
        safe_value(row.get("Experience Years")),
        safe_value(row.get("English Level")),
        safe_value(row.get("Highlights")),
        safe_value(row.get("CV")),
    ]

    return "\n".join(parts)


cv_texts = df.apply(build_cv_text, axis=1).tolist()

print(f"Loading model: {MODEL_NAME}")

model = SentenceTransformer(
    MODEL_NAME,
    device=device
)

print("Model loaded!")
print("Model device:", model.device)

print("=" * 80)
print("Creating BGE-M3 CV embeddings...")
print(f"Batch size: {BATCH_SIZE}")
print("=" * 80)

with torch.inference_mode():

    cv_embeddings = model.encode(
        cv_texts,
        batch_size=BATCH_SIZE,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=True
    )

print("=" * 80)
print("Embeddings shape:", cv_embeddings.shape)

np.save(
    OUTPUT_EMBEDDINGS_PATH,
    cv_embeddings
)

print(f"Saved embeddings to: {OUTPUT_EMBEDDINGS_PATH}")
print("=" * 80)