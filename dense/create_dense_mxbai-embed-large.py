import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

DATA_PATH = "data/candidate_profiles_20k.parquet"
EMBEDDINGS_PATH = "data/cv_embeddings_mxbai_embed_large.npy"

MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1"
BATCH_SIZE = 64

device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using device: {device}")

if device == "cuda":
    print(f"GPU: {torch.cuda.get_device_name(0)}")

df = pd.read_parquet(DATA_PATH)
print("Rows:", len(df))

print(f"Loading model: {MODEL_NAME}")
model = SentenceTransformer(MODEL_NAME, device=device)
print("Model loaded!")

texts = df["CV"].fillna("").astype(str).tolist()

embeddings = model.encode(
    texts,
    batch_size=BATCH_SIZE,
    normalize_embeddings=True,
    convert_to_numpy=True,
    show_progress_bar=True
)

np.save(EMBEDDINGS_PATH, embeddings)

print("Done!")
print("Shape:", embeddings.shape)
print("Saved to:", EMBEDDINGS_PATH)