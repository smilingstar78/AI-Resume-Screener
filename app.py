import streamlit as st
import pandas as pd
from main import analyze_resume

# Page Config
st.set_page_config(
    page_title="Resume Intel AI",
    layout="wide",
    page_icon="🎯"
)

# ---------------- MODERN STYLING ----------------
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Card design */
    .res-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    .res-card:hover {
        border-color: #38bdf8;
        transform: translateY(-2px);
    }
    
    /* Metrics */
    .metric-text {
        font-size: 24px;
        font-weight: bold;
        color: #38bdf8;
    }
    
    /* Skills Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin-right: 5px;
        margin-bottom: 5px;
        font-weight: 500;
    }
    .matched { background-color: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid #22c55e; }
    .missing { background-color: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR INPUTS ----------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4616/4616734.png", width=80)
    st.title("Control Panel")
    job_description = st.text_area("🎯 Job Requirements", placeholder="Paste the job description here...", height=250)
    
    uploaded_files = st.file_uploader(
        "📂 Candidate Resumes",
        type=["pdf"],
        accept_multiple_files=True
    )
    
    st.info("Upload PDF resumes to rank candidates against the job description.")

# ---------------- MAIN CONTENT ----------------
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🎯 Resume Intel AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Advanced Semantic Matching & Skill Gap Analysis</p>", unsafe_allow_html=True)
st.write("---")

if uploaded_files and job_description:
    results = []
    
    with st.spinner("Analyzing resumes using NLP..."):
        for file in uploaded_files:
            # We don't need to write to disk if we use a buffer, 
            # but sticking to your logic for simplicity:
            with open(file.name, "wb") as f:
                f.write(file.getbuffer())
            
            result = analyze_resume(file.name, job_description)
            results.append({
                "resume": file.name,
                "score": result["score"],
                "matched": result["matched_skills"],
                "missing": result["missing_skills"]
            })

    # Sort results
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    # ---------------- TOP CANDIDATE ----------------
    st.subheader("🏆 Best Match")
    top = results[0]
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
            <div class="res-card" style="text-align: center;">
                <p style="color: #94a3b8; margin-bottom: 0;">MATCH SCORE</p>
                <div class="metric-text" style="font-size: 48px;">{top['score']}%</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"### {top['resume']}")
        st.progress(top['score'] / 100)
        
        # Display Badges
        matched_html = "".join([f'<span class="badge matched">{s}</span>' for s in top['matched']])
        missing_html = "".join([f'<span class="badge missing">{s}</span>' for s in top['missing']])
        
        st.markdown(f"**Matched:** {matched_html}", unsafe_allow_html=True)
        st.markdown(f"**Missing:** {missing_html}", unsafe_allow_html=True)

    st.write("---")

    # ---------------- ALL CANDIDATES TABLE/CARDS ----------------
    st.subheader("📊 Candidate Ranking")
    
    for r in results[1:]: # Showing others below
        with st.container():
            c1, c2, c3 = st.columns([2, 1, 3])
            with c1:
                st.markdown(f"**{r['resume']}**")
            with c2:
                st.markdown(f"<span style='color:#38bdf8; font-weight:bold;'>{r['score']}% Match</span>", unsafe_allow_html=True)
            with c3:
                # Mini badges for the list
                m_html = "".join([f'<span class="badge matched" style="font-size:10px;">{s}</span>' for s in r['matched'][:3]])
                st.markdown(m_html + ("..." if len(r['matched']) > 3 else ""), unsafe_allow_html=True)
            st.markdown("<div style='height:1px; background:rgba(255,255,255,0.1); margin:10px 0;'></div>", unsafe_allow_html=True)

else:
    st.warning("Please paste a Job Description and upload Resumes to begin analysis.")