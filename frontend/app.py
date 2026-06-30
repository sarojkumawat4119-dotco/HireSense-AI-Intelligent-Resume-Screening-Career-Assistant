import streamlit as st

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
        st.success("✅ Files uploaded successfully!")
        st.info("Analyzing Resume... (Coming in next phase)")