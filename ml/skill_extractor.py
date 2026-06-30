import re
from ml.skills import TECHNICAL_SKILLS


def preprocess_text(text):
    """
    Convert text to lowercase and remove extra spaces.
    """
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text


def extract_skills(text):
    """
    Extract technical skills from resume/JD text.

    Parameters
    ----------
    text : str

    Returns
    -------
    list
        List of detected skills
    """

    if not text:
        return []

    processed_text = preprocess_text(text)

    extracted_skills = []

    for skill in TECHNICAL_SKILLS:

        if skill.lower() in processed_text:
            extracted_skills.append(skill)

    # Remove duplicates and sort
    extracted_skills = sorted(list(set(extracted_skills)))

    return extracted_skills