import os
import json
from groq import Groq

GROQ_MODEL = "openai/gpt-oss-120b"

def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set. Please add it to your .env file.")
    return Groq(api_key=api_key)

def extract_structured_info(text, doc_type="resume"):
    prompt = f"""Extract structured information from this {doc_type}.
Return ONLY valid JSON, no extra commentary, in exactly this shape:
{{"skills": ["..."], "experience_years": "...", "education": "...", "key_requirements": ["..."]}}

{doc_type.capitalize()} text:
{text[:3000]}"""

    client = get_groq_client()
    resp = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    raw = resp.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"skills": [], "experience_years": "", "education": "", "key_requirements": [], "_raw": raw}

def compute_skill_match_score(resume_info, jd_info):
    resume_skills = set(s.lower().strip() for s in resume_info.get("skills", []))
    jd_skills = set(s.lower().strip() for s in jd_info.get("key_requirements", []) + jd_info.get("skills", []))
    if not jd_skills:
        return 0.0, set()
    matched = resume_skills & jd_skills
    return round(len(matched) / len(jd_skills) * 100, 1), matched

def compute_final_score(ats_score, semantic_score, skill_match_score):
    return round(ats_score * 0.25 + semantic_score * 0.45 + skill_match_score * 0.30, 1)

print("Skill match + final score functions ready.")
