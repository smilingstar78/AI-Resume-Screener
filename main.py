from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, util

# Load real AI model (this is the key upgrade)
model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------- PDF TEXT ----------------
def extract_text_from_pdf(pdf_path):
    pdf = PdfReader(pdf_path)
    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


# ---------------- SCORE (REAL AI) ----------------
def get_match_score(resume_text, job_text):
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_text, convert_to_tensor=True)

    score = util.cos_sim(resume_embedding, job_embedding)[0][0]

    return float(score) * 100


# ---------------- ANALYZE ----------------
def analyze_resume(pdf_path, job_description):
    resume_text = extract_text_from_pdf(pdf_path)

    score = get_match_score(resume_text, job_description)

    return score