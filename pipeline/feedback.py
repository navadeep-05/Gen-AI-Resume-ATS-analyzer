import os
from groq import Groq

GROQ_MODEL = "openai/gpt-oss-120b"

def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set. Please add it to your .env file.")
    return Groq(api_key=api_key)

def generate_feedback(resume_text, jd_text, ats_score, semantic_score, skill_match_score, final_score, missing_keywords):
    prompt = f"""You are an ATS optimization expert and career coach.

Resume (excerpt): {resume_text[:2000]}
Job description (excerpt): {jd_text[:1500]}

Scores:
- ATS keyword score: {ats_score}/100
- Semantic similarity score: {semantic_score}/100
- Skill match score: {skill_match_score}/100
- Final weighted score: {final_score}/100

Missing keywords/skills: {', '.join(list(missing_keywords)[:15])}

Provide the feedback strictly using the following concise, structured markdown format (use tables where specified). Do not add any introductory or concluding fluff.

### 1. Overall fit assessment
[2-3 sentences evaluating the fit based on the scores and keywords]

### 2. Top 5 resume improvements (ranked by impact)
|   | What to change    |    Why it matters  |
|---|---|---|
| 1 | [Ultra-short change]    |    [Simple reason] |
| 2 | [Ultra-short change]    |    [Simple reason] |
| 3 | [Ultra-short change]    |    [Simple reason] |
| 4 | [Ultra-short change]    |    [Simple reason] |
| 5 | [Ultra-short change]    |    [Simple reason] |


### 3. One rewritten bullet point (before -> after)
**Before**
- [Weak bullet from the resume]

**After**
- [Strong, quantified, keyword-rich bullet]

*Why it works:*
- [Reason 1]
- [Reason 2]

### 4. Skills to learn / highlight for interview success
| Category | Specific Skills (List max 3) | How to showcase (Max 10 words) |
|--- | --- | ---|
| [Category] | [Skill 1, Skill 2] | [Ultra-short advice] |
"""
    client = get_groq_client()
    resp = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return resp.choices[0].message.content

print("Feedback generation function ready.")