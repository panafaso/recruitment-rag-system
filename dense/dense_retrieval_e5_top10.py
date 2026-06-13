import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

DATA_PATH = "../data/candidate_profiles_20k.parquet"
EMBEDDINGS_PATH = "../data/cv_embeddings_multilingual_e5_large.npy"
OUTPUT_PATH = "../embeddings + results/dense_multilingual_e5_large_results_top10.md"

MODEL_NAME = "intfloat/multilingual-e5-large"
TOP_K = 10

device = "cuda" if torch.cuda.is_available() else "cpu"

print("=" * 80)
print(f"Using device: {device}")

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))

print("=" * 80)

df = pd.read_parquet(DATA_PATH)
print("Rows:", len(df))

cv_embeddings = np.load(EMBEDDINGS_PATH)
print("Embeddings shape:", cv_embeddings.shape)

assert len(df) == len(cv_embeddings), "Mismatch between dataset rows and embeddings!"

print(f"Loading model: {MODEL_NAME}")

model = SentenceTransformer(
    MODEL_NAME,
    device=device
)

print("Model loaded!")
print("Model device:", model.device)


def safe_value(x):
    return "" if pd.isna(x) else str(x)


def log(line, f):
    print(line)
    f.write(line + "\n")


def retrieve_dense(query, top_k=TOP_K):
    query_text = "query: " + query

    query_embedding = model.encode(
        [query_text],
        normalize_embeddings=True,
        convert_to_numpy=True
    )

    similarities = np.dot(query_embedding, cv_embeddings.T)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]

    return top_indices, similarities[top_indices]


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

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    log("# Dense Retrieval Results - multilingual-e5-large", f)
    log(f"\nModel: {MODEL_NAME}", f)
    log(f"Top K: {TOP_K}", f)

    for category, queries in query_categories.items():
        log("\n" + "#" * 100, f)
        log(f"## Category: {category}", f)
        log("#" * 100, f)

        for query in queries:
            log(f"\n### Query: {query}", f)
            log(f"\nTOP {TOP_K} DENSE RESULTS:\n", f)

            top_indices, top_scores = retrieve_dense(query)

            for rank, (idx, score) in enumerate(zip(top_indices, top_scores), start=1):
                row = df.iloc[idx]

                log("---", f)
                log(f"### Rank {rank}", f)
                log(f"- Similarity: {score:.4f}", f)
                log(f"- Dataset Index: {idx}", f)
                log(f"- Candidate ID: {safe_value(row.get('id', row.get('ID', idx)))}", f)
                log(f"- Position: {safe_value(row.get('Position'))}", f)
                log(f"- Primary Keyword: {safe_value(row.get('Primary Keyword'))}", f)
                log(f"- Experience Years: {safe_value(row.get('Experience Years'))}", f)
                log(f"- English Level: {safe_value(row.get('English Level'))}", f)

                log("\n#### Highlights", f)
                log(safe_value(row.get("Highlights")), f)

                log("\n#### CV snippet", f)
                log(safe_value(row.get("CV")), f)

                log("", f)

print(f"\nResults saved to: {OUTPUT_PATH}")