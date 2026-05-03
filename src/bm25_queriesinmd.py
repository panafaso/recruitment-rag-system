import pandas as pd
import numpy as np
import re
from rank_bm25 import BM25Okapi

# Load dataset
df = pd.read_parquet("data/candidate_profiles_20k.parquet")

print("Rows:", len(df))
print("Columns:", df.columns.tolist())


# Safe value
def safe_value(x):
    return "" if pd.isna(x) else str(x)


# Log (terminal + file)
def log(line, f):
    print(line)
    f.write(line + "\n")


# Build BM25 text
def build_retrieval_text(row):
    return f"""
    Moreinfo: {safe_value(row.get("Moreinfo"))}
    Highlights: {safe_value(row.get("Highlights"))}
    English Level: {safe_value(row.get("English Level"))}
    Experience Years: {safe_value(row.get("Experience Years"))}
    CV: {safe_value(row.get("CV"))}
    """


texts = df.apply(build_retrieval_text, axis=1).tolist()


# Tokenizer
def tokenize(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9+#. ]", " ", text)
    return text.split()


tokenized_corpus = [tokenize(doc) for doc in texts]


# BM25 index
print("Building BM25 index...")
bm25 = BM25Okapi(tokenized_corpus)
print("BM25 ready!")


# Retrieval function
def retrieve_bm25(query, top_k=5):
    tokenized_query = tokenize(query)
    scores = bm25.get_scores(tokenized_query)

    top_indices = np.argsort(scores)[::-1][:top_k]

    return top_indices, scores[top_indices]


# Queries
query_categories = {
    "General Role-Based Queries": [
        "Software engineer with 5+ years experience",
        "Frontend developer with React expertise"
    ],
    "Skills-Focused Queries": [
        "Candidates skilled in Python and machine learning",
        "Cybersecurity experts with penetration testing experience"
    ],
    "Experience Level Queries": [
        "Mid-level project managers with 3 to 5 years experience",
        "Experienced legal consultants with 10+ years experience"
    ],
    "Industry-Specific Queries": [
        "Healthcare professionals with clinical experience",
        "Fintech engineers with blockchain exposure"
    ],
    "Location-Based Queries": [
        "Developers based in Europe",
        "Remote customer support agents"
    ],
    "Education & Certification Queries": [
        "AWS-certified solutions architects",
        "Candidates with cybersecurity certifications"
    ],
    "Soft Skills & Traits Queries": [
        "Candidates with strong leadership skills",
        "Professionals with excellent communication skills"
    ],
    "Tools & Technologies Queries": [
        "Developers using Docker and Kubernetes",
        "QA testers using Selenium"
    ],
    "Combination / Advanced Queries": [
        "Python developers with fintech experience in Europe",
        "AI engineers with NLP project experience"
    ],
    "Edge Cases & Specific Filters": [
        "Multilingual candidates with English Greek and French",
        "Candidates with no degree but strong experience"
    ]
}


# Write results
def write_results_md(query, top_indices, top_scores, f):
    log(f"\n### Query: {query}", f)
    log("\nTOP BM25 RESULTS:\n", f)

    for rank, (idx, score) in enumerate(zip(top_indices, top_scores), start=1):
        row = df.iloc[idx]

        log("---", f)
        log(f"**Rank {rank}**", f)
        log(f"- **BM25 Score:** {score:.4f}", f)
        log(f"- **Dataset Index:** {idx}", f)
        log(f"- **Candidate ID:** {safe_value(row.get('id', row.get('ID', idx)))}", f)
        log(f"- **Position:** {safe_value(row.get('Position'))}", f)
        log(f"- **Primary Keyword:** {safe_value(row.get('Primary Keyword'))}", f)
        log(f"- **Experience Years:** {safe_value(row.get('Experience Years'))}", f)
        log(f"- **English Level:** {safe_value(row.get('English Level'))}", f)

        log("\n**Highlights:**", f)
        log(safe_value(row.get("Highlights")), f)

        log("\n**CV snippet:**", f)
        log(safe_value(row.get("CV"))[:500], f)
        log("", f)


# Main
if __name__ == "__main__":
    top_k = 5
    output_path = "bm25_results.md"

    with open(output_path, "w", encoding="utf-8") as f:

        log("# BM25 Retrieval Results\n", f)

        for category, queries in query_categories.items():
            log("\n" + "#" * 100, f)
            log(f"## Category: {category}", f)
            log("#" * 100, f)

            for query in queries:
                top_indices, top_scores = retrieve_bm25(query, top_k=top_k)
                write_results_md(query, top_indices, top_scores, f)

    print(f"\nResults saved to {output_path}")