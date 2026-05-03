import pandas as pd
import numpy as np
import re
from rank_bm25 import BM25Okapi


# Load candidate dataset
df = pd.read_parquet("data/candidate_profiles_20k.parquet")

print("Rows:", len(df))
print("Columns:", df.columns.tolist())



# Convert missing values to empty text

def safe_value(x):
    return "" if pd.isna(x) else str(x)



# Build text for BM25

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



# Build BM25 index

print("Building BM25 index...")
bm25 = BM25Okapi(tokenized_corpus)
print("BM25 ready!")



# BM25 retrieval function
def retrieve_bm25(query, top_k=5):
    tokenized_query = tokenize(query)
    scores = bm25.get_scores(tokenized_query)

    top_indices = np.argsort(scores)[::-1][:top_k]

    return top_indices, scores[top_indices]


# Multiple queries
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


# Print results
def print_results(query, top_indices, top_scores):
    print("\nQUERY:", query)
    print("\nTOP BM25 RESULTS:\n")

    for rank, (idx, score) in enumerate(zip(top_indices, top_scores), start=1):
        row = df.iloc[idx]

        print("=" * 80)
        print(f"Rank: {rank}")
        print(f"BM25 Score: {score:.4f}")
        print("Dataset Index:", idx)

        print("Candidate ID:", safe_value(row.get("id", row.get("ID", idx))))
        print("Position:", safe_value(row.get("Position")))
        print("Primary Keyword:", safe_value(row.get("Primary Keyword")))
        print("Experience Years:", safe_value(row.get("Experience Years")))
        print("English Level:", safe_value(row.get("English Level")))
        print("Highlights:", safe_value(row.get("Highlights")))

        print("\nCV snippet:")
        print(safe_value(row.get("CV"))[:500])
        print()



# Run all queries
if __name__ == "__main__":
    top_k = 5

    for category, queries in query_categories.items():
        print("\n" + "#" * 100)
        print("CATEGORY:", category)
        print("#" * 100)

        for query in queries:
            top_indices, top_scores = retrieve_bm25(query, top_k=top_k)
            print_results(query, top_indices, top_scores)