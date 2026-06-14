import pandas as pd
import requests
import re
import time
import json


HYBRID_PATH = "../data/hybrid_rrf_rankings_bm25plus_bgem3.csv"
CANDIDATES_PATH = "../data/candidate_profiles_20k.parquet"

OUTPUT_CSV = "../data/llm_listwise_mistral_top5.csv"
OUTPUT_MD = "../data/llm_listwise_mistral_report.md"


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_SHOW_URL = "http://localhost:11434/api/show"

MODEL_NAME = "mistral:7b-instruct"


WINDOW_SIZE = 4
STRIDE = 2
PASSES = 2
FINAL_TOP_N = 5

# None = send full CV text to the LLM
MAX_CV_CHARS_FOR_LLM = None

# Only for the markdown report, to keep it readable
MAX_CV_CHARS_FOR_REPORT = 2500



query_texts = {
    "software_engineering": "Senior software engineers with 5+ years experience in backend systems cloud infrastructure and microservices",
    "frontend_development": "Frontend React developers with TypeScript Redux Next.js and responsive web application experience",
    "machine_learning_ai": "Junior Python machine learning engineers with TensorFlow PyTorch NLP and FastAPI experience",
    "cybersecurity": "Cybersecurity engineers with penetration testing OWASP vulnerability assessment and SIEM experience",
    "legal_compliance": "Experienced legal consultants with 7+ experience in data protection, AML compliance and cybersecurity",
    "project_management": "Project managers with Agile Scrum Jira stakeholder management and up to 4 years experience",
    "hr_recruitment": "HR recruiters with IT hiring onboarding sourcing and candidate interview experience",
    "customer_support_success": "Customer success managers with 3-6 years of experience and B2B SaaS client retention onboarding and communication skills",
    "marketing": "Digital marketing specialists with SEO Google Analytics content marketing and campaign management experience",
    "sales_business_development": "Business development managers with B2B sales negotiation partnership building and international client experience",
    "ui_ux_design": "UI UX designers with Figma prototyping user research and mobile application design experience",
    "blockchain_fintech": "Fintech software engineers with blockchain cryptocurrency smart contract and payment systems experience",
    "operations_management": "Operations managers with experience in process optimization budgeting team coordination reporting and business operations",
    "soft_skills_multilingual": "Multilingual professionals speaking English Greek French and German with client facing communication experience",
    "soft_skills_leadership": "Professionals with leadership mentoring stakeholder management and cross functional collaboration skills",
    "junior_trainee_queries": "Junior professionals and trainees looking for entry level opportunities with internship project or early career experience",
}


def safe_text(x):
    if pd.isna(x):
        return ""
    return str(x)


def get_candidate_id(row):
    for col in ["id", "ID", "candidate_id"]:
        if col in row:
            return str(row[col]).strip()
    return None


def build_candidate_text(row, max_chars=None):
    text = f"""
Position: {safe_text(row.get("Position"))}
Primary Keyword: {safe_text(row.get("Primary Keyword"))}
Experience Years: {safe_text(row.get("Experience Years"))}
English Level: {safe_text(row.get("English Level"))}

Highlights:
{safe_text(row.get("Highlights"))}

CV:
{safe_text(row.get("CV"))}
"""

    if max_chars is None:
        return text

    return text[:max_chars]


def md_escape(text):
    text = safe_text(text)
    return text.replace("\r\n", "\n").replace("\r", "\n")


def get_ollama_model_info():
    try:
        response = requests.post(
            OLLAMA_SHOW_URL,
            json={"model": MODEL_NAME},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        info_lines = []
        info_lines.append(f"Model name requested: {MODEL_NAME}")

        if "model_info" in data:
            info_lines.append("Model info:")
            info_lines.append(json.dumps(data["model_info"], indent=2)[:3000])

        if "details" in data:
            info_lines.append("Details:")
            info_lines.append(json.dumps(data["details"], indent=2)[:3000])

        if "modified_at" in data:
            info_lines.append(f"Modified at: {data['modified_at']}")

        return "\n".join(info_lines)

    except Exception as e:
        return f"Could not retrieve Ollama model info. Error: {e}"


def call_mistral(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    response.raise_for_status()
    return response.json().get("response", "").strip()


def parse_order(answer, window_ids):
    """
    Parses answers like this example:
    [2] > [1] > [4] > [3]
    or
    2,1,4,3

    Returns the corresponding candidate_ids.
    """

    numbers = re.findall(r"\b[1-4]\b", answer)

    ordered = []
    for n in numbers:
        idx = int(n) - 1
        if 0 <= idx < len(window_ids):
            cid = window_ids[idx]
            if cid not in ordered:
                ordered.append(cid)

    missing = [cid for cid in window_ids if cid not in ordered]

    return ordered + missing


def rank_window_with_llm(query, window_ids, candidate_text_lookup):
    resumes_section = ""

    for i, cid in enumerate(window_ids, start=1):
        resumes_section += f"\n\nCandidate [{i}]\n"
        resumes_section += f"Internal candidate ID: {cid}\n"
        resumes_section += candidate_text_lookup.get(cid, "")

    prompt = f"""
You are an expert technical recruiter.

You must rerank a small group of candidates for the job requirement.

IMPORTANT:
The current order comes from a retrieval system, but it may be wrong.
Do NOT preserve the original order by default.
Actively compare the candidates and change the order if another candidate is a better fit.

Job requirement:
{query}

Candidates:
{resumes_section}

Evaluate each candidate based ONLY on explicit evidence in the CV.

Focus on:
- Required technical skills
- Matching years of experience
- Relevant domain expertise
- Matching tools, frameworks, and technologies
- Responsibilities related to the role
- Language and soft skills only if requested

Rules:
- Do NOT assume skills that are not mentioned.
- Do NOT reward generic experience.
- Prefer direct evidence of the requested qualifications.
- Rank from BEST match to WORST match.

Return ONLY the final ranking using candidate numbers.

Required format:
[2] > [1] > [4] > [3]
"""

    answer = call_mistral(prompt)

    print("\nRAW MISTRAL ANSWER:")
    print(answer)
    print("-" * 80)

    parsed_order = parse_order(answer, window_ids)

    return parsed_order, answer


def sliding_window_rerank(query, candidate_ids, candidate_text_lookup):
    """
    ConFit-style listwise sliding-window reranking:
    - window size = 4
    - stride = 2
    - passes = 2
    """

    current_order = candidate_ids.copy()
    logs = []

    for pass_num in range(1, PASSES + 1):
        print(f"  Pass {pass_num}/{PASSES}")

        starts = list(
            range(
                0,
                len(current_order) - WINDOW_SIZE + 1,
                STRIDE
            )
        )

        for start in starts:
            end = start + WINDOW_SIZE
            input_window = current_order[start:end].copy()

            output_window, raw_answer = rank_window_with_llm(
                query=query,
                window_ids=input_window,
                candidate_text_lookup=candidate_text_lookup
            )

            current_order[start:end] = output_window

            logs.append({
                "pass": pass_num,
                "start": start + 1,
                "end": end,
                "input_window": input_window,
                "llm_answer": raw_answer,
                "output_window": output_window.copy(),
                "current_order": current_order.copy()
            })

            print(
                f"    Window {start + 1}-{end}: "
                f"{input_window} -> {output_window}"
            )

            time.sleep(0.2)

    return current_order, logs


hybrid = pd.read_csv(HYBRID_PATH)
candidates = pd.read_parquet(CANDIDATES_PATH)

hybrid["query_id"] = hybrid["query_id"].astype(str).str.strip()
hybrid["candidate_id"] = hybrid["candidate_id"].astype(str).str.strip()
hybrid["rank"] = hybrid["rank"].astype(int)

candidates["candidate_id"] = candidates.apply(get_candidate_id, axis=1)
candidates["candidate_id"] = candidates["candidate_id"].astype(str).str.strip()

candidate_text_lookup_llm = {
    row["candidate_id"]: build_candidate_text(row, MAX_CV_CHARS_FOR_LLM)
    for _, row in candidates.iterrows()
}

candidate_text_lookup_report = {
    row["candidate_id"]: build_candidate_text(row, MAX_CV_CHARS_FOR_REPORT)
    for _, row in candidates.iterrows()
}

candidate_original_info = {}

for _, row in hybrid.iterrows():
    candidate_original_info[(row["query_id"], row["candidate_id"])] = {
        "original_rank": int(row["rank"]),
        "original_rrf_score": float(row["score"])
    }

model_info = get_ollama_model_info()

final_rows = []
md_lines = []

md_lines.append("# Mistral Listwise Sliding-Window Reranking Report\n")
md_lines.append("## Configuration\n")
md_lines.append(f"- Model: `{MODEL_NAME}`")
md_lines.append(f"- Input rankings: `{HYBRID_PATH}`")
md_lines.append(f"- Candidate profiles: `{CANDIDATES_PATH}`")
md_lines.append(f"- Output CSV: `{OUTPUT_CSV}`")
md_lines.append(f"- Window size: `{WINDOW_SIZE}`")
md_lines.append(f"- Stride: `{STRIDE}`")
md_lines.append(f"- Passes: `{PASSES}`")
md_lines.append(f"- Final output: Top-{FINAL_TOP_N}")
md_lines.append(f"- Max CV characters sent to LLM: `{MAX_CV_CHARS_FOR_LLM}`")
md_lines.append(f"- Max CV characters shown in report: `{MAX_CV_CHARS_FOR_REPORT}`")
md_lines.append(f"- Ollama endpoint: `{OLLAMA_URL}`\n")

md_lines.append("## Ollama Model Information\n")
md_lines.append("```text")
md_lines.append(model_info)
md_lines.append("```\n")

md_lines.append("## Method\n")
md_lines.append(
    "The Hybrid RRF Top-10 candidates are reranked using a listwise sliding-window strategy. "
    "For each query, Mistral receives windows of 4 candidate CVs and ranks them from best to worst. "
    "The window moves with stride 2, and the full procedure is repeated for 2 passes. "
    "The final Top-5 candidates are retained for evaluation.\n"
)

for query_id, group in hybrid.groupby("query_id"):
    print(f"\nReranking query: {query_id}")

    query = query_texts.get(query_id)

    if query is None:
        raise ValueError(f"Missing query text for query_id: {query_id}")

    group = group.sort_values("rank")
    initial_order = group["candidate_id"].tolist()

    final_order, logs = sliding_window_rerank(
        query=query,
        candidate_ids=initial_order,
        candidate_text_lookup=candidate_text_lookup_llm
    )

    top5 = final_order[:FINAL_TOP_N]

    md_lines.append("\n---\n")
    md_lines.append(f"## Query ID: `{query_id}`\n")
    md_lines.append(f"**Job query:** {query}\n")

    md_lines.append("### Original Hybrid Top-10\n")
    for cid in initial_order:
        info = candidate_original_info[(query_id, cid)]
        md_lines.append(
            f"- Rank {info['original_rank']}: `{cid}` "
            f"(RRF score: {info['original_rrf_score']:.6f})"
        )

    md_lines.append("\n### Sliding-window LLM decisions\n")
    for log in logs:
        md_lines.append(
            f"\n#### Pass {log['pass']}, window {log['start']}-{log['end']}\n"
            f"- Input window: `{log['input_window']}`\n"
            f"- Raw Mistral answer: `{md_escape(log['llm_answer'])}`\n"
            f"- Parsed output window: `{log['output_window']}`\n"
            f"- Current order after window: `{log['current_order']}`\n"
        )

    md_lines.append("\n### Final Mistral Listwise Top-5\n")

    for new_rank, cid in enumerate(top5, start=1):
        info = candidate_original_info[(query_id, cid)]

        final_rows.append({
            "query_id": query_id,
            "system": "Hybrid_RRF_BM25Plus_BGE-M3_Mistral_Listwise_Top5",
            "rank": new_rank,
            "score": FINAL_TOP_N - new_rank + 1,
            "candidate_id": cid,
            "original_rank": info["original_rank"],
            "original_rrf_score": info["original_rrf_score"]
        })

        md_lines.append(
            f"{new_rank}. `{cid}` "
            f"(original rank: {info['original_rank']}, "
            f"RRF score: {info['original_rrf_score']:.6f})"
        )

    md_lines.append("\n### Candidate CV snippets shown for inspection\n")

    for cid in top5:
        md_lines.append(f"\n#### Candidate `{cid}`\n")
        md_lines.append("```text")
        md_lines.append(md_escape(candidate_text_lookup_report.get(cid, "")))
        md_lines.append("```")


final_df = pd.DataFrame(final_rows)

final_df.to_csv(OUTPUT_CSV, index=False)

with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print("\nSaved CSV:")
print(OUTPUT_CSV)

print("\nSaved Markdown report:")
print(OUTPUT_MD)

print("\nPreview:")
print(final_df.head(20))