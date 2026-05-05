import streamlit as st
from main import analyze_resume

st.set_page_config(page_title="AI Resume Screener", layout="centered")

st.title("🤖 AI Resume Screener (Real ATS)")

job_description = st.text_area("📄 Paste Job Description")

uploaded_file = st.file_uploader("📤 Upload Resume (PDF)", type=["pdf"])


# ---------------- SESSION STATE ----------------
if "decision" not in st.session_state:
    st.session_state.decision = None


if uploaded_file and job_description:

    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    score = analyze_resume("temp.pdf", job_description)

    # ---------------- SCORE ----------------
    st.subheader("📊 Match Score")
    st.write(f"**{score:.2f}%**")

    if score > 70:
        st.success("Strong Match ✅")
    elif score > 50:
        st.warning("Medium Match ⚠️")
    else:
        st.error("Weak Match ❌")

    # ---------------- ACTION BUTTONS ----------------
    st.subheader("🎯 Recruiter Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✅ Shortlist"):
            st.session_state.decision = "shortlisted"

    with col2:
        if st.button("❌ Reject"):
            st.session_state.decision = "rejected"

    with col3:
        if st.button("📌 Hold"):
            st.session_state.decision = "hold"


    # ---------------- SHOW RESULT ----------------
    if st.session_state.decision:
        st.info(f"Final Decision: {st.session_state.decision.upper()}")