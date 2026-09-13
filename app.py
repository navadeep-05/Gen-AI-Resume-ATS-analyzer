import os
import shutil
import tempfile
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import pipeline functions in specified order
from pipeline.extract import extract_resume_text
from pipeline.jd_input import get_jd_text
from pipeline.structured import extract_structured_info, compute_skill_match_score, compute_final_score
from pipeline.ats_score import compute_ats_score
from pipeline.similarity import compute_semantic_score
from pipeline.feedback import generate_feedback

app = FastAPI(title="AI Resume & ATS Analyzer")

# Create static directory if it doesn't exist
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/analyze")
async def analyze_resume(
    resume_file: UploadFile = File(...),
    jd_type: str = Form("text"),
    jd_text: str = Form(None),
    jd_url: str = Form(None)
):
    if not resume_file or not resume_file.filename:
        return JSONResponse(status_code=400, content={"error": "Please select a resume file (PDF or image)."})

    suffix = os.path.splitext(resume_file.filename)[1].lower()
    if suffix not in [".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".webp"]:
        return JSONResponse(
            status_code=400,
            content={"error": f"Unsupported file extension '{suffix}'. Please upload a PDF or an image (PNG, JPG)."}
        )

    # 1. Save uploaded file temporarily and extract text
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(resume_file.file, tmp)
            tmp_path = tmp.name

        resume_extracted_text = extract_resume_text(tmp_path)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": f"Failed to read resume file: {str(e)}"}
        )
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

    if not resume_extracted_text or len(resume_extracted_text.strip()) < 10:
        return JSONResponse(
            status_code=400,
            content={"error": "Could not extract readable text from your resume. If it's a scanned PDF, please upload a clear image or digital PDF."}
        )

    # 2. Process Job Description input
    jd_input_val = jd_text if jd_type == "text" else jd_url
    if not jd_input_val or not jd_input_val.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Please provide a Job Description (either text or URL)."}
        )

    try:
        jd_extracted_text = get_jd_text(jd_input_val)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": f"Error retrieving Job Description: {str(e)}"}
        )

    if not jd_extracted_text:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Could not fetch job description from the provided URL. Popular job boards (LinkedIn, Indeed) often block automated scrapers. Please copy and paste the job text directly."
            }
        )

    # 3. Scoring & Extraction Pipeline
    try:
        resume_info = extract_structured_info(resume_extracted_text, "resume")
        jd_info = extract_structured_info(jd_extracted_text, "job description")
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"AI extraction error: {str(e)}. Please check if GROQ_API_KEY is correctly set in .env."}
        )

    try:
        ats_score, matched_kw, missing_kw = compute_ats_score(resume_extracted_text, jd_extracted_text)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"ATS Keyword analysis error: {str(e)}"}
        )

    try:
        semantic_score = compute_semantic_score(resume_extracted_text, jd_extracted_text)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Semantic similarity evaluation error: {str(e)}"}
        )

    try:
        skill_match_score, matched_skills = compute_skill_match_score(resume_info, jd_info)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Skill matching computation error: {str(e)}"}
        )

    final_score = compute_final_score(ats_score, semantic_score, skill_match_score)

    # 4. Feedback Generation
    try:
        feedback = generate_feedback(
            resume_extracted_text,
            jd_extracted_text,
            ats_score,
            semantic_score,
            skill_match_score,
            final_score,
            missing_kw
        )
    except Exception as e:
        feedback = f"### AI Feedback Status\n\nFeedback generation skipped or unavailable: {str(e)}\n\nPlease ensure your `GROQ_API_KEY` is configured in `.env`."

    return JSONResponse(content={
        "status": "success",
        "ats_score": ats_score,
        "semantic_score": semantic_score,
        "skill_match_score": skill_match_score,
        "final_score": final_score,
        "missing_keywords": sorted(list(missing_kw))[:25],
        "matched_keywords": sorted(list(matched_kw))[:15],
        "resume_info": resume_info,
        "jd_info": jd_info,
        "feedback": feedback
    })
