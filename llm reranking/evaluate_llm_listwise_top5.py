import pandas as pd
import numpy as np


LLM_PATH = "../data/llm_listwise_mistral_top5.csv"
QRELS_PATH = "../data/qrels_annotations_top10_final.xlsx"

OUTPUT_PER_QUERY = "../data/metrics_llm_listwise_top5_per_query.csv"
OUTPUT_SUMMARY = "../data/metrics_llm_listwise_top5_summary.csv"


def precision_at_k(binary_rels, k):
    return sum(binary_rels[:k]) / k


def recall_at_k(binary_rels, total_relevant, k):
    if total_relevant == 0:
        return 0.0

    return sum(binary_rels[:k]) / total_relevant


def average_precision_at_k(binary_rels, k):
    score = 0.0
    hits = 0

    for i, rel in enumerate(binary_rels[:k], start=1):
        if rel == 1:
            hits += 1
            score += hits / i

    if hits == 0:
        return 0.0

    return score / hits


def reciprocal_rank_at_k(binary_rels, k):
    for i, rel in enumerate(binary_rels[:k], start=1):
        if rel == 1:
            return 1 / i

    return 0.0


def ndcg_at_k(binary_rels, k):
    rels = binary_rels[:k]

    ideal = sorted(rels, reverse=True)

    dcg = np.sum(
        np.array(rels, dtype=float)
        /
        np.log2(np.arange(2, len(rels) + 2))
    )

    idcg = np.sum(
        np.array(ideal, dtype=float)
        /
        np.log2(np.arange(2, len(ideal) + 2))
    )

    if idcg == 0:
        return 0.0

    return dcg / idcg


llm = pd.read_csv(LLM_PATH)

qrels = pd.read_excel(QRELS_PATH)

qrels = qrels[
    ["query_id", "candidate_id", "relevance"]
]


eval_df = llm.merge(
    qrels,
    on=["query_id", "candidate_id"],
    how="left"
)

eval_df["relevance"] = eval_df["relevance"].fillna(0)

per_query_results = []

for query_id, group in eval_df.groupby("query_id"):

    group = group.sort_values("rank")

    relevances = group["relevance"].tolist()

    # relevance==2 
    binary_rels = [
        1 if rel == 2 else 0
        for rel in relevances
    ]

    total_relevant = qrels[
        (qrels["query_id"] == query_id)
        &
        (qrels["relevance"] == 2)
    ]["candidate_id"].nunique()

    row = {
        "query_id": query_id,
        "system": "Hybrid_RRF_BM25Plus_BGE-M3_Mistral_Listwise_Top5",

        "Precision@5":
            precision_at_k(binary_rels, 5),

        "Recall@5":
            recall_at_k(binary_rels, total_relevant, 5),

        "MAP@5":
            average_precision_at_k(binary_rels, 5),

        "MRR@5":
            reciprocal_rank_at_k(binary_rels, 5),

        "NDCG@5":
            ndcg_at_k(binary_rels, 5),
    }

    per_query_results.append(row)


per_query_df = pd.DataFrame(per_query_results)

summary_df = (
    per_query_df
    .drop(columns=["query_id"])
    .groupby("system")
    .mean()
    .reset_index()
)

per_query_df.to_csv(
    OUTPUT_PER_QUERY,
    index=False
)

summary_df.to_csv(
    OUTPUT_SUMMARY,
    index=False
)


print("\n===== LLM LISTWISE RESULTS =====\n")

print(summary_df.to_string(index=False))

print("\nSaved files:")

print(OUTPUT_PER_QUERY)
print(OUTPUT_SUMMARY)