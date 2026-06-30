import sys
from pathlib import Path

# ---------------------------
# Add project root to Python path
# ---------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# ---------------------------
# Imports
# ---------------------------
import streamlit as st
from ml.parser import extract_text
from ml.skill_extractor import extract_skills
from ml.similarity import compare_skills
from ml.ats_score import calculate_ats_score
from ml.gemini_service import generate_feedback
# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="HireSense AI",
    page_icon="📄",
    layout="centered"
)

# ---------------------------
# Header
# ---------------------------
st.title("📄 HireSense AI")
st.subheader("AI Resume Screening & Career Assistant")

st.markdown("---")

st.header("👤 Student Dashboard")

# ---------------------------
# Resume Upload
# ---------------------------
resume_file = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf", "docx"]
)

# ---------------------------
# Job Description Upload
# ---------------------------
jd_file = st.file_uploader(
    "📋 Upload Job Description (Optional)",
    type=["pdf", "docx", "txt"]
)

st.markdown("### OR")

jd_text = st.text_area(
    "✍️ Paste Job Description",
    height=200,
    placeholder="Paste the job description here..."
)

st.markdown("---")

# ---------------------------
# Analyze Button
# ---------------------------
if st.button("🚀 Analyze Resume", use_container_width=True):

    if resume_file is None:
        st.error("Please upload your resume.")

    elif jd_file is None and jd_text.strip() == "":
        st.error("Please upload or paste a Job Description.")

    else:

        # -----------------------------
        # Extract Resume Text
        # -----------------------------
        resume_text = extract_text(resume_file)

        # -----------------------------
        # Extract Job Description Text
        # -----------------------------
        if jd_file:
            jd_text_content = extract_text(jd_file)
        else:
            jd_text_content = jd_text

        # -----------------------------
        # Extract Skills
        # -----------------------------
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text_content)

        # -----------------------------
        # Compare Skills
        # -----------------------------
        comparison = compare_skills(resume_skills, jd_skills)
        ats_score, breakdown = calculate_ats_score(
            comparison,
            resume_text,
            jd_text_content
        )
        # -----------------------------
        # ATS Score
        # -----------------------------
        st.header("🎯 ATS Score")

        st.metric(
            "Overall ATS Score",
            f"{ats_score}/100"
        )

        st.subheader("📊 Score Breakdown")

        st.write(breakdown)
        # -----------------------------
        # Success Message
        # -----------------------------
        st.success("✅ Files uploaded successfully!")

        # -----------------------------
        # Display Resume Text
        # -----------------------------
        st.subheader("📄 Extracted Resume")

        st.text_area(
            "Resume Text",
            resume_text,
            height=250
        )

        # -----------------------------
        # Display Job Description
        # -----------------------------
        st.subheader("📋 Extracted Job Description")

        st.text_area(
            "Job Description",
            jd_text_content,
            height=250
        )

        # -----------------------------
        # Display Resume Skills
        # -----------------------------
        st.subheader("🧠 Resume Skills")
        st.write(resume_skills)

        # -----------------------------
        # Display JD Skills
        # -----------------------------
        st.subheader("📌 Job Description Skills")
        st.write(jd_skills)
        feedback = generate_feedback(
            resume_text,
            jd_text_content,
            ats_score,
            comparison["matched"],
            comparison["missing"]
        )
        st.header("🤖 AI Resume Feedback")

        st.write(feedback)
        # -----------------------------
        # Skill Comparison
        # -----------------------------
        st.subheader("✅ Matched Skills")
        st.write(comparison["matched"])

        st.subheader("❌ Missing Skills")
        st.write(comparison["missing"])

        st.subheader("⭐ Extra Skills")
        st.write(comparison["extra"])

        # -----------------------------
        # Skill Match Percentage
        # -----------------------------
        st.metric(
            label="📊 Skill Match Percentage",
            value=f"{comparison['match_percentage']}%"
        )