import re
import logging
from pathlib import Path
from typing import List

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, util


# ---------------- CONFIG ----------------
logging.basicConfig(level=logging.INFO)

model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------- SKILL DATABASE ----------------
SKILL_PATTERNS = {
    "python": [r"\bpython\b"],
    "machine learning": [r"\bmachine learning\b", r"\bml\b"],
    "deep learning": [r"\bdeep learning\b", r"\bdl\b"],
    "nlp": [r"\bnlp\b", r"\bnatural language processing\b"],
    "sql": [r"\bsql\b"],
    "pandas": [r"\bpandas\b"],
    "numpy": [r"\bnumpy\b"],
    "tensorflow": [r"\btensorflow\b", r"\btensor flow\b"],
    "pytorch": [r"\bpytorch\b", r"\bpy torch\b"],
    "flask": [r"\bflask\b"],
    "fastapi": [r"\bfastapi\b"],
    "git": [r"\bgit\b"],
    "docker": [r"\bdocker\b"],
    "api": [r"\bapi\b"],
    "aws": [r"\baws\b"],
    "azure": [r"\bazure\b"],
    "java": [r"\bjava\b"],
    "react": [r"\breact\b"],
    "javascript": [r"\bjavascript\b", r"\bjs\b"],
    "scikit-learn": [r"\bscikit\b", r"\bsklearn\b"],
    "tableau": [r"\btableau\b"],
    "power bi": [r"\bpower bi\b"],
    "c++": [r"\bc\+\+\b"],
    "mongodb": [r"\bmongodb\b"]
}


# ---------------- PDF EXTRACTION ----------------
def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        pdf = PdfReader(pdf_path)

        pages = []

        for page in pdf.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    except Exception as e:
        logging.error(f"PDF extraction error: {e}")
        return ""


# ---------------- TEXT CHUNKING ----------------
def chunk_text(text: str, chunk_size: int = 500) -> List[str]:

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


# ---------------- SEMANTIC MATCH ----------------
def get_semantic_score(resume_text: str, job_text: str):

    if not resume_text or not job_text:
        return 0.0

    chunks = chunk_text(resume_text)

    job_embedding = model.encode(
        job_text,
        convert_to_tensor=True
    )

    scores = []

    for chunk in chunks:

        chunk_embedding = model.encode(
            chunk,
            convert_to_tensor=True
        )

        score = util.cos_sim(
            chunk_embedding,
            job_embedding
        )[0][0]

        scores.append(float(score))

    if not scores:
        return 0.0

    best_score = max(scores)

    return round(best_score * 100, 2)


# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text: str):

    text = text.lower()

    found = set()

    for skill, patterns in SKILL_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, text):
                found.add(skill)
                break

    return found


# ---------------- EXPLANATION ----------------
def generate_explanation(score, matched, missing):

    if score > 80:
        fit = "Excellent fit"
    elif score > 60:
        fit = "Good fit"
    elif score > 40:
        fit = "Moderate fit"
    else:
        fit = "Low fit"

    return (
        f"{fit}. "
        f"Matched {len(matched)} required skills. "
        f"Missing {len(missing)} skills."
    )


# ---------------- MAIN ----------------
def analyze_resume(pdf_path, job_text):

    resume_text = extract_text_from_pdf(pdf_path)

    semantic_score = get_semantic_score(
        resume_text,
        job_text
    )

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_text
    )

    matched = sorted(
        list(
            resume_skills & job_skills
        )
    )

    missing = sorted(
        list(
            job_skills - resume_skills
        )
    )

    explanation = generate_explanation(
        semantic_score,
        matched,
        missing
    )

    return {
        "score": semantic_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "explanation": explanation
    }
