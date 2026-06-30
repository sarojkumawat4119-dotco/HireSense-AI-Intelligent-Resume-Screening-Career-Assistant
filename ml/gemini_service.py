import os
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai

# Load .env from project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Check your .env file."
    )

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_feedback(
    resume_text,
    jd_text,
    ats_score,
    matched_skills,
    missing_skills,
):

    prompt = f"""
You are an ATS Resume Expert.

Resume:
{resume_text}

Job Description:
{jd_text}

ATS Score:
{ats_score}

Matched Skills:
{matched_skills}

Missing Skills:
{missing_skills}

Provide your response in this format:

## Resume Strengths

## Resume Weaknesses

## Missing Skills

## Suggested Projects

## Certifications to Learn

## Final Recommendation

Keep the response concise and actionable.
"""

    response = model.generate_content(prompt)

    return response.text