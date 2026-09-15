from sentence_transformers import SentenceTransformer, util

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def compute_semantic_score(resume_text, jd_text):
    model = get_model()
    r_emb = model.encode(resume_text, convert_to_tensor=True)
    j_emb = model.encode(jd_text, convert_to_tensor=True)
    return round(util.cos_sim(r_emb, j_emb).item() * 100, 1)

print("SBERT model module ready.")
