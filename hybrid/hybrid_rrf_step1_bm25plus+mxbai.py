import pandas as pd
from collections import defaultdict

RANKINGS_PATH = "../data/rankings_all_models_top10_final.csv"

df = pd.read_csv(RANKINGS_PATH)

print("Before filtering:")
print(df["system"].unique())
print(df.shape)

df = df[df["system"].isin(["BM25Plus", "MXBAI"])]

print("\nAfter filtering:")
print(df["system"].unique())
print(df.shape)

K = 60
hybrid_rows = []

for query_id, group in df.groupby("query_id"):
    scores = defaultdict(float)

    for system, sys_group in group.groupby("system"):
        sys_group = sys_group.sort_values("rank")

        for _, row in sys_group.iterrows():
            doc_id = row["candidate_id"]
            rank = int(row["rank"])
            scores[doc_id] += 1 / (K + rank)

    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    for new_rank, (doc_id, rrf_score) in enumerate(ranked_docs[:10], start=1):
        hybrid_rows.append({
            "query_id": query_id,
            "system": "Hybrid_RRF_BM25Plus_MXBAI",
            "rank": new_rank,
            "score": rrf_score,
            "candidate_id": doc_id
        })

hybrid_df = pd.DataFrame(hybrid_rows)

hybrid_df.to_csv("../data/hybrid_rrf_rankings_bm25plus_mxbai.csv", index=False)

print("Hybrid RRF rankings saved to ../data/hybrid_rrf_rankings_bm25plus_mxbai.csv")
print(hybrid_df.head(20))