from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, util

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text_from_pdf(pdf_path):
    try:
        pdf = PdfReader(pdf_path)
        text = ""

        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text

    except:
        return ""


# ---------------- SEMANTIC SCORE ----------------
def get_score(resume_text, job_text):

    if not resume_text or not job_text:
        return 0.0

    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    job_emb = model.encode(job_text, convert_to_tensor=True)

    score = util.cos_sim(resume_emb, job_emb)[0][0]

    return round(float(score) * 100, 2)


# ---------------- SKILL DATABASE ----------------
SKILLS_DB = {
    "python", "machine learning", "deep learning", "nlp",
    "sql", "pandas", "numpy", "tensorflow", "pytorch",
    "flask", "fastapi", "git", "docker", "api",
    "aws", "azure", "java", "react", "javascript",
    "scikit-learn", "tableau", "power bi", "c++", "mongodb"
}


# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text):
    text = text.lower()

    found = set()
    for skill in SKILLS_DB:
        if skill in text:
            found.add(skill)

    return found


# ---------------- MAIN FUNCTION ----------------
def analyze_resume(pdf_path, job_text):

    resume_text = extract_text_from_pdf(pdf_path)

    score = get_score(resume_text, job_text)

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matched = list(resume_skills & job_skills)
    missing = list(job_skills - resume_skills)

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing
    }