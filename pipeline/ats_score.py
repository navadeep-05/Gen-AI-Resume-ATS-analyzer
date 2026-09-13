import re
from collections import Counter

# Expanded stopwords list to filter out generic language and generic job description filler
STOPWORDS = {
    "the", "and", "for", "with", "this", "that", "are", "you", "will", "have",
    "from", "your", "our", "who", "what", "where", "when", "why", "how",
    "a", "an", "is", "in", "it", "of", "to", "on", "as", "at", "by", "or",
    "be", "we", "can", "not", "all", "but", "if", "they", "their", "them",
    "about", "any", "which", "there", "so", "up", "out", "more", "has", "do",
    "been", "would", "should", "could", "these", "those", "into", "through",
    "some", "such", "only", "over", "also", "most", "than", "then", "other",
    # Resume/Job specific generic words
    "experience", "work", "role", "company", "team", "job", "skills",
    "years", "looking", "required", "requirements", "knowledge", "ability",
    "including", "using", "strong", "working", "support", "provide",
    "ensure", "business", "development", "management", "new", "help",
    "good", "best", "make", "sure", "related", "equivalent", "opportunity",
    "join", "part", "time", "full", "candidate", "candidates", "must",
    "preferred", "plus", "understanding", "excellent", "written", "verbal",
    "skills", "demonstrated", "environment", "fast", "paced", "track", "record",
    "projects", "data", "solutions", "design", "build", "process", "processes",
    "within", "across", "complex", "system", "systems", "high", "quality"
}

def extract_keywords(text, top_n=40):
    # Extract alphanumeric words (allowing +, #, . for terms like C++, C#, .NET)
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.]{2,}\b", text.lower())
    words = [w for w in words if w not in STOPWORDS]
    return set(w for w, _ in Counter(words).most_common(top_n))

def compute_ats_score(resume_text, jd_text):
    # We want to identify the core ~40 keywords of the JD
    jd_kw = extract_keywords(jd_text, top_n=40)
    
    # We extract more keywords from the resume, because a resume is longer 
    # and might have a wider spread of word frequencies. If a word appears 
    # in the resume, it should count towards matching the JD.
    resume_kw = extract_keywords(resume_text, top_n=150)
    
    if not jd_kw:
        return 0.0, set(), set()
        
    matched = resume_kw & jd_kw
    missing = jd_kw - resume_kw
    
    ats_score = round(len(matched) / len(jd_kw) * 100, 1)
    return ats_score, matched, missing

print("ATS scoring ready.")