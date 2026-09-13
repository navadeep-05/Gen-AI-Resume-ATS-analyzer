import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
    except Exception:
        pass

    if len(text.strip()) < 50:  # likely scanned/image-based PDF
        try:
            images = convert_from_path(pdf_path)
            ocr_text = "\n".join(pytesseract.image_to_string(img) for img in images)
            if ocr_text.strip():
                text = ocr_text
        except Exception:
            pass

    return text.strip()

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        return pytesseract.image_to_string(img).strip()
    except Exception:
        return ""

def extract_resume_text(file_path):
    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    else:
        return extract_text_from_image(file_path)

print("Resume extraction functions ready.")