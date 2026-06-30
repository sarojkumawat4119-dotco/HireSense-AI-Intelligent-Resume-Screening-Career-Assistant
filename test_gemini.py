from ml.gemini_service import generate_feedback

feedback = generate_feedback(
    resume_text="Python SQL Machine Learning",
    jd_text="Python SQL AWS Docker",
    ats_score=75,
    matched_skills=["Python", "SQL"],
    missing_skills=["AWS", "Docker"]
)

print(feedback)