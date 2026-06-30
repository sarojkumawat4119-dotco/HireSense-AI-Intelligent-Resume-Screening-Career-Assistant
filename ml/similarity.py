def compare_skills(resume_skills, jd_skills):
    """
    Compare resume skills with job description skills.
    """

    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = sorted(list(resume_set.intersection(jd_set)))
    missing = sorted(list(jd_set - resume_set))
    extra = sorted(list(resume_set - jd_set))

    if len(jd_set) == 0:
        match_percentage = 0
    else:
        match_percentage = round((len(matched) / len(jd_set)) * 100, 2)

    return {
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "match_percentage": match_percentage
    }