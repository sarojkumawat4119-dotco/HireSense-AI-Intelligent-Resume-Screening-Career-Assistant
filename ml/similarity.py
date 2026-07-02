from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Load model once at import time
# (loading it per-request would be very slow)
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# How similar two skills need to be (0-1) to count as a match.
# 1.0 = identical wording. Real synonyms usually land 0.6-0.85.
# -----------------------------
SIMILARITY_THRESHOLD = 0.6


def compare_skills(resume_skills, jd_skills):
    """
    Compare resume skills with job description skills using
    semantic similarity instead of exact string matching.

    Returns the SAME shape as before:
    { "matched", "missing", "extra", "match_percentage" }
    """

    if not jd_skills:
        return {
            "matched": [],
            "missing": [],
            "extra": sorted(resume_skills),
            "match_percentage": 0
        }

    if not resume_skills:
        return {
            "matched": [],
            "missing": sorted(jd_skills),
            "extra": [],
            "match_percentage": 0
        }

    resume_embeddings = model.encode(resume_skills, convert_to_tensor=True)
    jd_embeddings = model.encode(jd_skills, convert_to_tensor=True)

    similarity_matrix = util.cos_sim(jd_embeddings, resume_embeddings)

    matched = []
    missing = []
    used_resume_skills = set()

    for i, jd_skill in enumerate(jd_skills):
        best_score, best_index = similarity_matrix[i].max(dim=0)
        best_score = best_score.item()
        best_index = best_index.item()

        if best_score >= SIMILARITY_THRESHOLD:
            matched.append(jd_skill)
            used_resume_skills.add(resume_skills[best_index])
        else:
            missing.append(jd_skill)

    extra = [
        skill for skill in resume_skills
        if skill not in used_resume_skills
    ]

    matched = sorted(matched)
    missing = sorted(missing)
    extra = sorted(extra)

    match_percentage = round((len(matched) / len(jd_skills)) * 100, 2)

    return {
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "match_percentage": match_percentage
    }


def calculate_document_similarity(resume_text, jd_text):
    """
    Compares the FULL resume text against the FULL job description
    text as two documents, using TF-IDF vectors + cosine similarity.

    This is different from compare_skills() above:
    - compare_skills looks at individual skill words/phrases
    - this looks at the overall writing/content relevance of the
      whole resume against the whole JD (wording, phrasing, context)

    Returns: similarity percentage (0-100)
    """

    if not resume_text or not jd_text:
        return 0

    vectorizer = TfidfVectorizer(stop_words="english")

    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    except ValueError:
        # Happens if text is empty after removing stop words
        return 0

    similarity_score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    # Convert numpy float64 -> plain Python float.
    # Without this, the value can't be saved to PostgreSQL
    # ("schema np does not exist" error).
    return round(float(similarity_score) * 100, 2)
