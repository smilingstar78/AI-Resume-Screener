from pypdf import PdfReader
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


# Extract PDF text
pdf = PdfReader("MY_CV.pdf")

data = ""

for page in pdf.pages:
    text = page.extract_text()

    if text:
        data += text + "\n"


# NLP processing
doc = nlp(data.lower())


# Clean tokens
clean_tokens = []

for token in doc:

    if (
        not token.is_stop
        and not token.is_punct
        and not token.is_space
    ):
        clean_tokens.append(token.lemma_)


# Convert tokens back to string
resume_text = " ".join(clean_tokens)


# Skills database
skills_db = {
    "python",
    "sql",
    "tensorflow",
    "pytorch",
    "machine learning",
    "deep learning",
    "pandas",
    "numpy",
    "scikit learn",
    "flask",
    "fastapi",
    "docker",
    "git"
}


# Find available skills
available = []

for skill in skills_db:

    if skill in resume_text:
        available.append(skill)


# Results
print("Skills found:")
print(available)


# Basic screening
if len(available) >= 5:
    print("Suitable for this Role!")
else:
    print("Not Suitable!")