import pandas as pd
import numpy as np
import re
from rank_bm25 import BM25Plus
from nltk.corpus import stopwords

DATA_PATH = "../data/candidate_profiles_20k.parquet"
OUTPUT_PATH = "bm25plus_stopwords_results_top10.md"
TOP_K = 10

K1 = 1.5
B = 0.60
DELTA = 1.0

df = pd.read_parquet(DATA_PATH)

print("Rows:", len(df))
print("Columns:", df.columns.tolist())


def safe_value(x):
    return "" if pd.isna(x) else str(x)


def log(line, f):
    print(line)
    f.write(line + "\n")


def build_retrieval_text(row):
    parts = [
        safe_value(row.get("Position")),
        safe_value(row.get("Primary Keyword")),
        safe_value(row.get("Moreinfo")),
        safe_value(row.get("Highlights")),
        safe_value(row.get("English Level")),
        safe_value(row.get("Experience Years")),
        safe_value(row.get("CV")),
    ]
    return "\n".join(parts)


texts = df.apply(build_retrieval_text, axis=1).tolist()

stop_words = set(stopwords.words("english"))

# Keep important recruitment words
important_words = {
    "no",
    "not",
    "more",
    "most"
}

stop_words = stop_words - important_words


def tokenize(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9+#. ]", " ", text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in stop_words]
    return tokens


print("Tokenizing corpus...")
tokenized_corpus = [tokenize(doc) for doc in texts]
print("Tokenization complete!")

print("Building BM25Plus index...")

bm25 = BM25Plus(
    tokenized_corpus,
    k1=K1,
    b=B,
    delta=DELTA
)

print("BM25Plus ready!")


def retrieve_bm25(query, top_k=TOP_K):
    tokenized_query = tokenize(query)
    scores = bm25.get_scores(tokenized_query)
    top_indices = np.argsort(scores)[::-1][:top_k]
    return top_indices, scores[top_indices]


query_categories = {
    "Software Engineering": [
        "Senior software engineers with 5+ years experience in backend systems cloud infrastructure and microservices"
    ],
    "Frontend Development": [
        "Frontend React developers with TypeScript Redux Next.js and responsive web application experience"
    ],
    "Machine Learning / AI": [
        "Junior Python machine learning engineers with TensorFlow PyTorch NLP and FastAPI experience"
    ],
    "Cybersecurity": [
        "Cybersecurity engineers with penetration testing OWASP vulnerability assessment and SIEM experience"
    ],
    "Legal / Compliance": [
        "Experienced legal consultants with 7+ experience in data protection, AML compliance and cybersecurity"
    ],
    "Project Management": [
        "Project managers with Agile Scrum Jira stakeholder management and up to 4 years experience"
    ],
    "HR / Recruitment": [
        "HR recruiters with IT hiring onboarding sourcing and candidate interview experience"
    ],
    "Customer Support / Success": [
        "Customer success managers with 3-6 years of experience and B2B SaaS client retention onboarding and communication skills"
    ],
    "Marketing": [
        "Digital marketing specialists with SEO Google Analytics content marketing and campaign management experience"
    ],
    "Sales / Business Development": [
        "Business development managers with B2B sales negotiation partnership building and international client experience"
    ],
    "UI / UX Design": [
        "UI UX designers with Figma prototyping user research and mobile application design experience"
    ],
    "Blockchain / Fintech": [
        "Fintech software engineers with blockchain cryptocurrency smart contract and payment systems experience"
    ],
    "Operations Management": [
        "Operations managers with experience in process optimization budgeting team coordination reporting and business operations"
    ],
    "Soft Skills": [
        "Multilingual professionals speaking English Greek French and German with client facing communication experience",
        "Professionals with leadership mentoring stakeholder management and cross functional collaboration skills"
    ],
    "Junior / Trainee Queries": [
        "Junior professionals and trainees looking for entry level opportunities with internship project or early career experience"
    ]
}


def write_results_md(query, top_indices, top_scores, f):
    log(f"\n### Query: {query}", f)
    log(f"\nTOP {TOP_K} BM25PLUS + STOPWORDS RESULTS:\n", f)

    for rank, (idx, score) in enumerate(zip(top_indices, top_scores), start=1):
        row = df.iloc[idx]

        candidate_id = safe_value(row.get("id", row.get("ID", idx)))

        log("---", f)
        log(f"### Rank {rank}", f)
        log(f"- BM25Plus Score: {score:.4f}", f)
        log(f"- Dataset Index: {idx}", f)
        log(f"- Candidate ID: {candidate_id}", f)
        log(f"- Position: {safe_value(row.get('Position'))}", f)
        log(f"- Primary Keyword: {safe_value(row.get('Primary Keyword'))}", f)
        log(f"- Experience Years: {safe_value(row.get('Experience Years'))}", f)
        log(f"- English Level: {safe_value(row.get('English Level'))}", f)

        log("\n#### Highlights", f)
        log(safe_value(row.get("Highlights")), f)

        log("\n#### CV snippet", f)
        log(safe_value(row.get("CV")), f)

        log("", f)


if __name__ == "__main__":
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        log("# BM25Plus + Stopwords Retrieval Results", f)
        log(f"\nTop K: {TOP_K}", f)
        log(f"k1: {K1}", f)
        log(f"b: {B}", f)
        log(f"delta: {DELTA}", f)
        log("Stopword removal: yes", f)
        log("Stemming: no", f)

        for category, queries in query_categories.items():
            log("\n" + "#" * 100, f)
            log(f"## Category: {category}", f)
            log("#" * 100, f)

            for query in queries:
                top_indices, top_scores = retrieve_bm25(query)
                write_results_md(query, top_indices, top_scores, f)

    print(f"\nResults saved to: {OUTPUT_PATH}")