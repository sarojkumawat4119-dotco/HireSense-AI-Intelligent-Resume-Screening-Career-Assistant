def calculate_ats_score(
    comparison,
    resume_text,
    jd_text
):
    """
    Calculate ATS Score based on different parameters.
    """

    score = 0
    breakdown = {}

    # ------------------------
    # Skill Match (40 Marks)
    # ------------------------
    skill_score = comparison["match_percentage"] * 0.4

    breakdown["Skill Match"] = round(skill_score, 2)

    score += skill_score

    # ------------------------
    # Projects (20 Marks)
    # ------------------------
    project_keywords = [
        "project",
        "developed",
        "built",
        "implemented"
    ]

    project_score = 0

    for word in project_keywords:
        if word.lower() in resume_text.lower():
            project_score += 5

    project_score = min(project_score, 20)

    breakdown["Projects"] = project_score

    score += project_score

    # ------------------------
    # Education (15 Marks)
    # ------------------------
    education_keywords = [
        "b.tech",
        "b.e",
        "bachelor",
        "master",
        "cgpa"
    ]

    education_score = 0

    for word in education_keywords:
        if word.lower() in resume_text.lower():
            education_score += 3

    education_score = min(education_score, 15)

    breakdown["Education"] = education_score

    score += education_score

    # ------------------------
    # Certifications (10 Marks)
    # ------------------------
    certification_keywords = [
        "certificate",
        "certification",
        "aws",
        "google",
        "azure"
    ]

    certification_score = 0

    for word in certification_keywords:
        if word.lower() in resume_text.lower():
            certification_score += 2

    certification_score = min(certification_score, 10)

    breakdown["Certifications"] = certification_score

    score += certification_score

    # ------------------------
    # Resume Quality (10 Marks)
    # ------------------------
    resume_quality = 10 if len(resume_text) > 1000 else 6

    breakdown["Resume Quality"] = resume_quality

    score += resume_quality

    # ------------------------
    # Keyword Density (5 Marks)
    # ------------------------
    keyword_density = 5 if comparison["match_percentage"] > 70 else 2

    breakdown["Keyword Density"] = keyword_density

    score += keyword_density

    return round(score, 2), breakdown